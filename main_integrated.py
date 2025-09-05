"""
整合版 AI Trading System
整合簡化版和完整版功能，適合Docker部署
包含Google OAuth、AI分析、用戶系統和配額管理
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import time
import urllib.parse
import secrets
import httpx
import logging
import sqlite3
import hashlib
import uuid
from datetime import datetime, timedelta
from dotenv import load_dotenv
import base64
from io import BytesIO

# 載入環境變數
load_dotenv()

# 導入統一配置管理
try:
    from config import (
        get_openai_client, 
        is_openai_configured,
        get_google_oauth_config,
        is_google_oauth_configured,
        get_app_config,
        validate_configuration
    )
    CONFIG_MODULE_AVAILABLE = True
except ImportError:
    # 向後兼容：如果配置模塊不存在，使用原始方式
    CONFIG_MODULE_AVAILABLE = False
    logger.warning("統一配置模塊不可用，使用傳統環境變數配置")

# 日誌設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置管理
if CONFIG_MODULE_AVAILABLE:
    # 使用統一配置
    app_config = get_app_config()
    google_config = get_google_oauth_config()
    
    # FastAPI 應用初始化
    app = FastAPI(
        title="AI Trading System - Integrated Edition",
        description="Professional AI-powered trading analysis platform with OAuth",
        version="2.0.0"
    )

    # CORS 設定
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_config.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 統一配置變數
    GOOGLE_CLIENT_ID = google_config.client_id
    GOOGLE_CLIENT_SECRET = google_config.client_secret
    GOOGLE_REDIRECT_URI = google_config.redirect_uri
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    JWT_SECRET = app_config.jwt_secret
    
else:
    # 向後兼容：原始配置方式
    app = FastAPI(
        title="AI Trading System - Integrated Edition", 
        description="Professional AI-powered trading analysis platform with OAuth",
        version="2.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:3001"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8080/api/auth/google/callback")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-here")

# OAuth 狀態管理
oauth_states = {}

# 認證設定
security = HTTPBearer(auto_error=False)

# 數據庫初始化
def init_database():
    """初始化SQLite資料庫"""
    conn = sqlite3.connect('trading.db')
    cursor = conn.cursor()
    
    # 用戶表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            google_id TEXT,
            full_name TEXT,
            avatar_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # 配額表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotas (
            user_id TEXT PRIMARY KEY,
            total_free_uses INTEGER DEFAULT 3,
            used_free_uses INTEGER DEFAULT 0,
            daily_used INTEGER DEFAULT 0,
            last_reset_date DATE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # 使用記錄表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_records (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            action_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # 兌換歷史表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS redemption_history (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            code TEXT,
            credits INTEGER,
            redeemed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# K線圖生成函數
def generate_candlestick_chart(symbol, hist_data, current_price, rsi, macd):
    """生成K線圖並返回base64編碼"""
    try:
        # 嘗試導入繪圖庫
        import matplotlib
        matplotlib.use('Agg')  # 非互動式後端
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from matplotlib.patches import Rectangle
        import numpy as np
        
        # 準備數據 - 取最近60天
        data = hist_data.tail(60).copy()
        if data.empty:
            return None
            
        # 創建圖表
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), 
                                     gridspec_kw={'height_ratios': [3, 1]}, 
                                     facecolor='#1e1e2e')
        
        # 設置深色主題
        plt.style.use('dark_background')
        ax1.set_facecolor('#1e1e2e')
        ax2.set_facecolor('#1e1e2e')
        
        # 設置中文字體支持
        try:
            plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
        except:
            pass  # 如果字體設置失敗就使用默認
        
        # K線圖
        dates = data.index
        opens = data['Open'].values
        highs = data['High'].values  
        lows = data['Low'].values
        closes = data['Close'].values
        
        # 繪製K線
        for i, (date, o, h, l, c) in enumerate(zip(dates, opens, highs, lows, closes)):
            color = '#00ff88' if c >= o else '#ff4444'
            
            # 影線
            ax1.plot([i, i], [l, h], color=color, linewidth=1, alpha=0.8)
            
            # K線實體
            height = abs(c - o)
            bottom = min(o, c)
            rect = Rectangle((i-0.3, bottom), 0.6, height, 
                           facecolor=color, alpha=0.8, edgecolor=color)
            ax1.add_patch(rect)
        
        # 移動平均線
        if len(data) >= 20:
            ma5 = data['Close'].rolling(5).mean()
            ma10 = data['Close'].rolling(10).mean() 
            ma20 = data['Close'].rolling(20).mean()
            
            ax1.plot(range(len(ma5)), ma5, color='#FFFF00', linewidth=1, alpha=0.7, label='MA5')
            ax1.plot(range(len(ma10)), ma10, color='#FFA500', linewidth=1, alpha=0.7, label='MA10')  
            ax1.plot(range(len(ma20)), ma20, color='#00FFFF', linewidth=1, alpha=0.7, label='MA20')
        
        # RSI子圖
        if len(data) >= 14:
            # 簡化RSI計算
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi_series = 100 - (100 / (1 + rs))
            
            ax2.plot(range(len(rsi_series)), rsi_series, color='#800080', linewidth=2)
            ax2.axhline(y=70, color='red', linestyle='--', alpha=0.5)
            ax2.axhline(y=30, color='green', linestyle='--', alpha=0.5)
            ax2.set_ylabel('RSI', color='white')
            ax2.set_ylim(0, 100)
        
        # 設置標題和標籤
        ax1.set_title(f'{symbol} - 股價走勢圖 (當前價格: ${current_price:.2f})', 
                     color='white', fontsize=14, pad=20)
        ax1.set_ylabel('價格 ($)', color='white')
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # 設置x軸標籤
        step = max(1, len(dates) // 8)
        x_ticks = range(0, len(dates), step)
        x_labels = [dates[i].strftime('%m-%d') for i in x_ticks]
        ax1.set_xticks(x_ticks)
        ax1.set_xticklabels(x_labels, color='white')
        ax2.set_xticks(x_ticks) 
        ax2.set_xticklabels(x_labels, color='white')
        
        # 調整佈局
        plt.tight_layout()
        
        # 轉為base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight', 
                   facecolor='#1e1e2e', edgecolor='none')
        buffer.seek(0)
        
        chart_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        plt.close(fig)
        
        return chart_base64
        
    except ImportError:
        logger.warning("Matplotlib not available, skipping chart generation")
        return None
    except Exception as e:
        logger.error(f"Chart generation error: {e}")
        return None

# 資料庫操作
class DatabaseManager:
    def get_connection(self):
        return sqlite3.connect('trading.db')
    
    def get_user_by_google_id(self, google_id: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE google_id = ?", (google_id,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def create_user(self, google_id: str, email: str, full_name: str, avatar_url: str = None):
        conn = self.get_connection()
        cursor = conn.cursor()
        user_id = str(uuid.uuid4())
        
        cursor.execute("""
            INSERT INTO users (id, email, google_id, full_name, avatar_url, last_login)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, email, google_id, full_name, avatar_url, datetime.utcnow()))
        
        # 創建配額記錄
        cursor.execute("""
            INSERT INTO quotas (user_id, total_free_uses, used_free_uses, daily_used, last_reset_date)
            VALUES (?, 3, 0, 0, DATE('now'))
        """, (user_id,))
        
        conn.commit()
        conn.close()
        return user_id
    
    def get_user_quota(self, user_id: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT total_free_uses, used_free_uses, daily_used, last_reset_date
            FROM quotas WHERE user_id = ?
        """, (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def update_quota_usage(self, user_id: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 檢查是否需要重置每日配額
        today = datetime.now().date()
        cursor.execute("SELECT last_reset_date FROM quotas WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        
        if result:
            last_reset = datetime.strptime(result[0], '%Y-%m-%d').date()
            if today > last_reset:
                cursor.execute("""
                    UPDATE quotas SET daily_used = 0, last_reset_date = DATE('now')
                    WHERE user_id = ?
                """, (user_id,))
        
        # 增加使用次數
        cursor.execute("""
            UPDATE quotas SET used_free_uses = used_free_uses + 1, daily_used = daily_used + 1
            WHERE user_id = ?
        """, (user_id,))
        
        # 記錄使用
        record_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO usage_records (id, user_id, action_type, created_at)
            VALUES (?, ?, 'ai_analysis', CURRENT_TIMESTAMP)
        """, (record_id, user_id))
        
        conn.commit()
        conn.close()

db = DatabaseManager()

# Pydantic 模型
class AnalysisRequest(BaseModel):
    symbol: str
    period: str = "3mo"
    include_ai: bool = True

class UserInfo(BaseModel):
    id: str
    email: str
    full_name: str
    avatar_url: Optional[str] = None
    remaining_free_uses: int
    daily_used: int

# JWT 處理 (簡化版)
def create_access_token(user_data: dict) -> str:
    """創建 JWT token"""
    import jwt
    payload = {
        "user_id": user_data["id"],
        "email": user_data["email"],
        "exp": datetime.utcnow() + timedelta(days=30)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def verify_token(token: str) -> Optional[dict]:
    """驗證 JWT token"""
    try:
        import jwt
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        return None

# 認證依賴
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """獲取當前用戶"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated"
        )
    
    token_data = verify_token(credentials.credentials)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"
        )
    
    return token_data

def can_use_ai_analysis(user_id: str) -> bool:
    """檢查用戶是否可以使用AI分析"""
    quota_info = db.get_user_quota(user_id)
    if not quota_info:
        return False
    
    total_free, used_free, daily_used, last_reset = quota_info
    
    # 檢查是否需要重置每日配額
    today = datetime.now().date()
    if last_reset:
        try:
            last_reset_date = datetime.strptime(last_reset, '%Y-%m-%d').date()
            if today > last_reset_date:
                # 需要重置，先更新數據庫
                conn = db.get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE quotas SET daily_used = 0, last_reset_date = DATE('now')
                    WHERE user_id = ?
                """, (user_id,))
                conn.commit()
                conn.close()
                daily_used = 0  # 重置後可以使用
        except (ValueError, TypeError):
            # 如果日期解析失敗，重置為今天
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE quotas SET daily_used = 0, last_reset_date = DATE('now')
                WHERE user_id = ?
            """, (user_id,))
            conn.commit()
            conn.close()
            daily_used = 0
    
    # 新用戶有免費機會
    if used_free < total_free:
        return True
    
    # 檢查每日配額 (每天1次)
    return daily_used < 1

# API 端點
@app.get("/")
async def root():
    return {
        "message": "🚀 AI Trading System - Integrated Edition",
        "status": "operational", 
        "version": "2.0.0",
        "features": ["stock_analysis", "ai_recommendations", "oauth_auth", "quota_system"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ai-trading-system-integrated",
        "timestamp": datetime.utcnow().isoformat(),
        "auth_configured": bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET),
        "ai_configured": is_openai_configured() if CONFIG_MODULE_AVAILABLE else bool(os.getenv("OPENAI_API_KEY"))
    }

@app.get("/test-chart/{symbol}")
async def test_chart_generation(symbol: str):
    """測試K線圖生成功能"""
    try:
        import yfinance as yf
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1mo")
        
        if hist.empty:
            return {"error": "No data available", "has_matplotlib": True}
        
        current_price = hist['Close'].iloc[-1]
        chart_base64 = generate_candlestick_chart(symbol, hist, current_price, 65.0, 2.5)
        
        return {
            "symbol": symbol,
            "data_points": len(hist),
            "current_price": current_price,
            "chart_generated": chart_base64 is not None,
            "chart_size": len(chart_base64) if chart_base64 else 0,
            "has_matplotlib": True
        }
    except Exception as e:
        return {"error": str(e), "has_matplotlib": False}

# Google OAuth 端點
@app.get("/api/auth/google/login")
async def google_login():
    """重定向到 Google OAuth 登入頁面"""
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google OAuth 未配置")
    
    state = secrets.token_urlsafe(32)
    oauth_states[state] = {"timestamp": time.time()}
    
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "scope": "openid email profile",
        "response_type": "code",
        "state": state,
        "access_type": "offline"
    }
    
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url=google_auth_url)

@app.get("/api/auth/google/callback")
async def google_callback(code: str = None, state: str = None, error: str = None):
    """處理 Google OAuth 回調"""
    if error:
        return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?error=oauth_denied")
    
    if not code or not state:
        return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?error=missing_params")
    
    if state not in oauth_states:
        return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?error=invalid_state")
    
    del oauth_states[state]
    
    try:
        async with httpx.AsyncClient() as client:
            # 交換 code 獲取 token
            token_data = {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": GOOGLE_REDIRECT_URI
            }
            
            token_response = await client.post("https://oauth2.googleapis.com/token", data=token_data)
            if token_response.status_code != 200:
                return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?error=token_exchange_failed")
            
            token_info = token_response.json()
            access_token = token_info.get("access_token")
            
            # 獲取用戶信息
            user_response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if user_response.status_code != 200:
                return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?error=user_info_failed")
            
            user_info = user_response.json()
            
            # 查找或創建用戶
            existing_user = db.get_user_by_google_id(user_info["id"])
            if existing_user:
                user_id = existing_user[0]
                user_name = existing_user[3]
            else:
                user_id = db.create_user(
                    google_id=user_info["id"],
                    email=user_info["email"],
                    full_name=user_info.get("name", ""),
                    avatar_url=user_info.get("picture")
                )
                user_name = user_info.get("name", "")
            
            # 創建 JWT token
            user_token = create_access_token({
                "id": user_id,
                "email": user_info["email"],
                "full_name": user_name
            })
            
            return RedirectResponse(
                url=f"{FRONTEND_URL}/auth/google/callback?login=success&token={user_token}&email={user_info['email']}&name={urllib.parse.quote(user_name or '')}"
            )
            
    except Exception as e:
        logger.error(f"OAuth error: {e}")
        return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?error=oauth_error")

@app.get("/api/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """獲取當前用戶信息"""
    quota_info = db.get_user_quota(current_user["user_id"])
    
    if quota_info:
        total_free, used_free, daily_used, _ = quota_info
        remaining_free = max(0, total_free - used_free)
        can_use_ai = can_use_ai_analysis(current_user["user_id"])
    else:
        remaining_free = 0
        daily_used = 0
        can_use_ai = False
    
    return {
        "id": current_user["user_id"],
        "email": current_user["email"],
        "full_name": current_user.get("full_name", ""),
        "is_premium": False,  # 暫時設為 False
        "remaining_initial_quota": remaining_free,
        "remaining_daily_quota": 1 - daily_used if daily_used < 1 else 0,
        "can_use_ai_analysis": can_use_ai
    }

# AI 分析端點
@app.post("/analyze/{symbol}")
async def analyze_stock(
    symbol: str,
    request: AnalysisRequest,
    current_user: dict = Depends(get_current_user)
):
    """股票AI分析 (需要認證和配額)"""
    
    # 檢查配額
    if not can_use_ai_analysis(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="AI分析配額已用完。新用戶有3次免費機會，之後每天可使用1次。"
        )
    
    # 消耗配額
    db.update_quota_usage(current_user["user_id"])
    
    # 增強版AI分析 - 整合分析師策略
    try:
        ai_available = is_openai_configured() if CONFIG_MODULE_AVAILABLE else bool(os.getenv("OPENAI_API_KEY"))
        if ai_available and request.include_ai:
            # 獲取股價數據用於分析
            import yfinance as yf
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(period="3mo")
                current_price = hist['Close'].iloc[-1] if not hist.empty else 100.0
                
                # 計算技術指標
                if len(hist) >= 20:
                    sma_5 = hist['Close'].rolling(window=5).mean().iloc[-1]
                    sma_10 = hist['Close'].rolling(window=10).mean().iloc[-1]
                    sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
                    volume_avg = hist['Volume'].rolling(window=20).mean().iloc[-1]
                    current_volume = hist['Volume'].iloc[-1]
                    
                    # RSI 計算
                    delta = hist['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi = 100 - (100 / (1 + rs)).iloc[-1]
                    
                    # MACD 計算
                    ema_12 = hist['Close'].ewm(span=12).mean().iloc[-1]
                    ema_26 = hist['Close'].ewm(span=26).mean().iloc[-1]
                    macd = ema_12 - ema_26
                else:
                    sma_5 = sma_10 = sma_20 = current_price
                    rsi = 50.0
                    macd = 0.0
                    volume_avg = current_volume = 1000000
            except Exception as e:
                logger.error(f"Error fetching stock data: {e}")
                current_price = 100.0
                sma_5 = sma_10 = sma_20 = current_price
                rsi = 50.0
                macd = 0.0
                volume_avg = current_volume = 1000000

            # 分析師策略AI提示
            analyst_prompt = f"""
            作為資深台股分析師，請基於以下數據為 {symbol} 提供專業分析：

            【股票數據】:
            - 當前價格: ${current_price:.2f}
            - 5日均線: ${sma_5:.2f}
            - 10日均線: ${sma_10:.2f}
            - 20日均線: ${sma_20:.2f}
            - RSI: {rsi:.1f}
            - MACD: {macd:.3f}
            - 成交量比: {(current_volume/volume_avg):.2f}

            【分析師策略核心招數】:

            1. 【RSI鈍化策略 - 分析師心法】:
               - 🚀 黃金策略: RSI > 80 且 KD > 80 = 強勢股繼續噴出 (不要反手放空)
               - 📈 進場訊號: RSI 20-30 反彈 + 日線不破低 = 絕佳買點
               - ⚠️ 風險提醒: RSI < 20 且持續破底 = 避開接刀子

            2. 【KD指標運用 - 分析師訣竅】:
               - 🎯 黃金交叉: K值上穿D值於20以下 = 反彈訊號
               - 🔴 死亡交叉: K值下穿D值於80以上 = 調整開始
               - 💡 鈍化判讀: 高檔鈍化看量縮，低檔鈍化看止跌

            3. 【MACD操作心法 - 分析師密技】:
               - ⚡ 紅棒轉強: DIF上穿MACD且紅棒放大 = 買進時機
               - 🌊 綠棒縮小: DIF接近MACD且綠棒縮減 = 築底完成
               - 🔍 綜合工具: 配合趨勢線、區間、月均線扣抵避免被巴來巴去

            4. 【均線分級應用 - 分析師心法】:
               - 🚀 噴出行情: 關注5日均線 (短線爆發)
               - 📈 波段操作: 觀察10日均線 (中期趨勢)
               - ⚡ 短線進出: 以5日均線為主要依據
               - 🌅 三陽開泰: 連續三根陽線突破，多頭確立
               - 🌃 三聲無奈: 連續三根陰線，空頭來臨
               - ✨ 買進條件: 股價站上5、10、20日均線並出現糾結

            5. 【三角收斂突破策略 - 分析師招數】:
               - 🟢 紅K突破: 紅K突破或跳空向上 → 趨勢朝上，可追價進場
               - 🔴 黑K跌破: 黑K慣性跌破或跳空向下 → 趨勢轉弱，應避開
               - 📊 量能確認: 收斂末端注意成交量放大確認突破
               - 🎯 進場時機: 三角形突破配合量增為最佳訊號

            6. 【分析師風險控管心法】:
               - 🛡️ 多重確認: RSI + 均線 + 成交量 + 型態 (絕不單一指標決策)
               - 🎯 停損設定: 依據前波低點或關鍵支撐 (分析師式風控)
               - 📊 量價健檢: 價漲量增=健康，價漲量縮=要小心
               - ⚠️ 避免套牢: 寧可錯過不可做錯，保持靈活進出

            **分析師策略核心理念**: 「站上均線買，跌破均線賣，配合RSI鈍化看KD，多重確認避免被巴」

            【視覺型態分析 - 圖表解讀招數】:
            7. 【K線型態識別 - 分析師看圖技巧】:
               - 📊 經典型態: 頭肩頂、雙重頂底、三角收斂、杯柄型態
               - 🔍 支撐阻力: 識別關鍵價位突破與回測
               - 📈 趨勢線分析: 上升/下降趨勢線的有效性
               - 🎯 缺口分析: 跳空缺口的方向性意義

            8. 【成交量型態 - 分析師量價配合】:
               - 🚀 放量突破: 價漲量增確認突破有效
               - 📉 縮量整理: 低量整理後的爆發力
               - ⚠️ 價量背離: 價格新高但量能萎縮的警訊

            請同時分析數據和K線圖，嚴格按照分析師完整招數提供分析，具體說明:
            1. 整體建議 (BUY/SELL/HOLD) - 基於分析師六大策略綜合判斷
            2. 信心水準 (0-1) - 多重確認後的信心度
            3. 關鍵推理 - 明確說明應用了哪些分析師具體招數
            4. 策略因子 - 列出符合的分析師策略要點
            5. 具體買進價位 - 精確計算進場價格 (必須提供數值)
            6. 具體停損價位 - 分析師風險管理原則計算的確切停損價 (必須提供數值)
            7. 目標價位 - 基於等幅上漲或支撐壓力的獲利目標
            8. 風險評估 (0-1) - 綜合分析師多重確認後的風險判斷

            **價位計算方法**:
            - 買進價位: 如果BUY→當前價±3%內的支撐位或突破價；如果HOLD→關鍵支撐價位
            - 停損價位: 前波低點或5日均線下緣-2%的保護價位
            - 目標價位: 等幅上漲或下一阻力位，風報比至少1:2

            **必須包含精確數值**: 所有價位都要具體到小數點後2位

            **重要**: 請提供詳細而完整的分析推理，包括：
            - 圖表型態的具體觀察
            - 支撐阻力位的識別
            - 成交量與價格的配合情況
            - 各項技術指標的綜合判斷
            - 風險因素的詳細說明

            Format as JSON: {{
              "recommendation": "BUY/SELL/HOLD",
              "confidence": 0.XX,
              "reasoning": "請提供至少200字的詳細分析推理，包括圖表觀察、技術指標判斷、風險評估等完整內容...",
              "key_factors": ["具體因子1", "具體因子2", "具體因子3", ...],
              "entry_price": XX.XX,
              "stop_loss": XX.XX, 
              "price_target": XX.XX,
              "risk_score": 0.XX
            }}
            """

            # 生成K線圖用於視覺分析
            chart_base64 = None
            try:
                chart_base64 = generate_candlestick_chart(symbol, hist, current_price, rsi, macd)
            except Exception as chart_error:
                logger.error(f"Chart generation error: {chart_error}")
            
            # 調用OpenAI API (升級為GPT-4o)
            if CONFIG_MODULE_AVAILABLE:
                client = get_openai_client()
            else:
                # 向後兼容
                import openai
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OpenAI API key not configured")
                client = openai.OpenAI(api_key=api_key)
            
            try:
                # 根據是否有圖表使用不同的API調用
                if chart_base64:
                    # 使用GPT-4o進行圖表分析 (新版本支持視覺)
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"你是資深股票分析師，專精於台股技術分析和策略制定。請同時分析以下數據和K線圖：\n\n{analyst_prompt}"},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{chart_base64}"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_tokens=2000,
                        temperature=0.3
                    )
                else:
                    # 使用GPT-3.5 Turbo進行數據分析
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "你是資深股票分析師，專精於台股技術分析和策略制定。"},
                            {"role": "user", "content": analyst_prompt}
                        ],
                        max_tokens=1000,
                        temperature=0.3
                    )
                
                ai_response = response.choices[0].message.content
                
                # 解析JSON回應
                try:
                    import json
                    # 提取JSON部分
                    json_start = ai_response.find('{')
                    json_end = ai_response.rfind('}') + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = ai_response[json_start:json_end]
                        ai_analysis = json.loads(json_str)
                    else:
                        raise ValueError("無法找到JSON格式")
                        
                except (json.JSONDecodeError, ValueError) as e:
                    logger.error(f"JSON parsing error: {e}")
                    logger.info(f"Raw AI response (first 500 chars): {ai_response[:500]}")
                    
                    # 如果是GPT-4 Vision的自然語言回應，嘗試提取關鍵信息
                    if "BUY" in ai_response.upper():
                        recommendation = "BUY"
                    elif "SELL" in ai_response.upper():
                        recommendation = "SELL"
                    else:
                        recommendation = "HOLD"
                    
                    # 備用分析，但包含更詳細的原始回應
                    ai_analysis = {
                        "recommendation": recommendation,
                        "confidence": 0.7,
                        "reasoning": ai_response[:500] if ai_response else "GPT-4 Vision分析完成，建議基於圖表和數據綜合考慮。",
                        "key_factors": ["GPT-4視覺分析", "技術指標綜合", "圖表型態識別"],
                        "entry_price": round(current_price * 0.98, 2),
                        "stop_loss": round(current_price * 0.95, 2),
                        "price_target": round(current_price * 1.05, 2),
                        "risk_score": 0.5
                    }
                    
            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
                ai_analysis = {
                    "recommendation": "HOLD",
                    "confidence": 0.5,
                    "reasoning": "AI分析暫時不可用，建議謹慎操作。",
                    "key_factors": ["API服務異常"],
                    "entry_price": round(current_price, 2),
                    "stop_loss": round(current_price * 0.95, 2),
                    "price_target": round(current_price * 1.03, 2),
                    "risk_score": 0.6
                }
        else:
            ai_analysis = {
                "login_required": True,
                "message": "需要登入才能使用AI分析功能"
            }
            
        return {
            "symbol": symbol,
            "analysis_time": datetime.utcnow().isoformat(),
            "ai_analysis": ai_analysis,
            "technical_indicators": {
                "current_price": current_price,
                "rsi": rsi,
                "macd": macd,
                "sma_5": sma_5,
                "sma_10": sma_10,
                "sma_20": sma_20,
                "volume_ratio": current_volume / volume_avg if 'volume_avg' in locals() else 1.0
            },
            "user_quota_used": True
        }
    
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail="分析服務暫時不可用")

@app.post("/api/auth/logout")
async def logout():
    """用戶登出"""
    return {"message": "登出成功", "status": "logged_out"}

# 兌換碼功能
class RedeemCodeRequest(BaseModel):
    code: str

@app.post("/api/redemption/redeem")
async def redeem_code(
    request: RedeemCodeRequest,
    current_user: dict = Depends(get_current_user)
):
    """兌換碼功能"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # 檢查兌換碼是否存在且有效
        cursor.execute("""
            SELECT id, credits, description, is_used, expires_at 
            FROM redemption_codes 
            WHERE code = ? AND is_active = 1
        """, (request.code.upper(),))
        
        code_data = cursor.fetchone()
        
        if not code_data:
            raise HTTPException(status_code=404, detail="兌換碼不存在或已失效")
        
        code_id, credits, description, is_used, expires_at = code_data
        
        if is_used:
            raise HTTPException(status_code=400, detail="此兌換碼已被使用")
        
        # 檢查是否過期
        if expires_at:
            from datetime import datetime
            expire_date = datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S.%f")
            if datetime.utcnow() > expire_date:
                raise HTTPException(status_code=400, detail="兌換碼已過期")
        
        # 標記兌換碼為已使用
        cursor.execute("""
            UPDATE redemption_codes 
            SET is_used = 1, used_by_user_id = ?, used_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (current_user["user_id"], code_id))
        
        # 更新用戶配額 - 正確的做法是減少已使用次數或增加總次數
        cursor.execute("""
            UPDATE quotas 
            SET total_free_uses = total_free_uses + ?,
                used_free_uses = MAX(0, used_free_uses - ?)
            WHERE user_id = ?
        """, (credits, credits, current_user["user_id"]))
        
        # 記錄兌換歷史
        cursor.execute("""
            INSERT INTO redemption_history (user_id, code_id, credits_added, redeemed_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (current_user["user_id"], code_id, credits))
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": f"兌換成功！獲得 {credits} 次AI分析機會",
            "credits_added": credits,
            "description": description
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Redemption error: {e}")
        raise HTTPException(status_code=500, detail="兌換處理失敗")

@app.get("/api/redemption")
async def redemption_info():
    """兌換碼系統信息"""
    return {
        "message": "兌換碼系統已就緒",
        "status": "available",
        "endpoints": {
            "redeem": "/api/redemption/redeem",
            "credits": "/api/redemption/credits",
            "history": "/api/redemption/history"
        }
    }

@app.get("/api/redemption/credits")
async def get_user_credits(current_user: dict = Depends(get_current_user)):
    """獲取用戶配額信息"""
    try:
        quota_info = db.get_user_quota(current_user["user_id"])
        if not quota_info:
            return {
                "bonus_credits": 0,
                "free_credits": 0,
                "daily_credits": 0,
                "total_credits": 0,
                "can_use_ai": False
            }
        
        total_free, used_free, daily_used, last_reset = quota_info
        
        # 檢查每日重置
        today = datetime.now().date()
        daily_available = 1 - daily_used
        if last_reset:
            try:
                last_reset_date = datetime.strptime(last_reset, '%Y-%m-%d').date()
                if today > last_reset_date:
                    daily_available = 1  # 重置後每日配額
            except (ValueError, TypeError):
                daily_available = 1
        
        remaining_free = max(0, total_free - used_free)
        total_available = remaining_free + max(0, daily_available)
        
        return {
            "bonus_credits": 0,  # 暫時沒有bonus系統
            "free_credits": remaining_free,
            "daily_credits": max(0, daily_available),
            "total_credits": total_available,
            "can_use_ai": total_available > 0
        }
    except Exception as e:
        logger.error(f"Get user credits error: {e}")
        raise HTTPException(status_code=500, detail="獲取配額信息失敗")

@app.get("/api/redemption/history")
async def get_redemption_history(current_user: dict = Depends(get_current_user)):
    """獲取用戶兌換歷史"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT rc.code, rh.credits_added, rh.redeemed_at, rc.description
            FROM redemption_history rh
            JOIN redemption_codes rc ON rh.code_id = rc.id
            WHERE rh.user_id = ?
            ORDER BY rh.redeemed_at DESC
        """, (current_user["user_id"],))
        
        history = []
        for row in cursor.fetchall():
            code, credits_added, redeemed_at, description = row
            history.append({
                "code": code,
                "credits_added": credits_added,
                "redeemed_at": redeemed_at,
                "description": description or f"{code} - {credits_added}次AI分析"
            })
        
        conn.close()
        return history
        
    except Exception as e:
        logger.error(f"Get redemption history error: {e}")
        raise HTTPException(status_code=500, detail="獲取兌換歷史失敗")

# 啟動時初始化資料庫
@app.on_event("startup")
async def startup_event():
    init_database()
    logger.info("Database initialized")
    logger.info(f"Google OAuth configured: {bool(GOOGLE_CLIENT_ID)}")
    
    if CONFIG_MODULE_AVAILABLE:
        logger.info(f"OpenAI API configured: {is_openai_configured()}")
        # 顯示配置驗證結果
        validation = validate_configuration()
        if validation['warnings']:
            for warning in validation['warnings']:
                logger.warning(warning)
        if validation['issues']:
            for issue in validation['issues']:
                logger.error(issue)
    else:
        logger.info(f"OpenAI API configured: {bool(os.getenv('OPENAI_API_KEY'))}")
        logger.warning("建議使用統一配置模塊以獲得更好的配置管理")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)