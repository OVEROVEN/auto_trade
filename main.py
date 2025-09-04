from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import time
import urllib.parse
import secrets
import httpx
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

app = FastAPI(
    title="AI Trading System",
    description="Professional AI-powered trading analysis platform",
    version="1.0.0"
)

# 添加 CORS 支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Google OAuth 配置
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET") 
GOOGLE_REDIRECT_URI = "http://localhost:8080/api/auth/google/callback"
FRONTEND_URL = "http://localhost:3000"

# 儲存臨時 OAuth 狀態
oauth_states = {}

@app.get("/")
async def root():
    return {
        "message": "🚀 AI Trading System is running!",
        "status": "operational", 
        "version": "1.0.0",
        "features": ["stock_analysis", "ai_recommendations", "redemption_codes"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ai-trading-system",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "timestamp": "2024-09-01T15:00:00Z"
    }

@app.get("/api/redemption")
async def redemption_info():
    return {
        "message": "兌換碼系統已就緒",
        "status": "available",
        "endpoints": {
            "redeem": "/api/redemption/redeem",
            "status": "/api/redemption/status"
        }
    }

@app.get("/docs-summary")
async def docs_summary():
    return {
        "api_documentation": "/docs",
        "health_check": "/health",
        "redemption_api": "/api/redemption",
        "auth_endpoints": "/api/auth",
        "interactive_docs": "/redoc"
    }

# OAuth 端點
@app.get("/api/auth/google/login")
async def google_login():
    """重定向到 Google OAuth 登入頁面"""
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google OAuth 未配置")
    
    # 生成隨機 state 參數
    state = secrets.token_urlsafe(32)
    oauth_states[state] = {"timestamp": time.time()}
    
    # 構建 Google OAuth URL
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
    
    # 驗證 state 參數
    if state not in oauth_states:
        return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?error=invalid_state")
    
    # 清理 state
    del oauth_states[state]
    
    try:
        # 交換 authorization code 獲取 access token
        async with httpx.AsyncClient() as client:
            token_data = {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": GOOGLE_REDIRECT_URI
            }
            
            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                data=token_data
            )
            
            if token_response.status_code != 200:
                return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?error=token_exchange_failed")
            
            token_info = token_response.json()
            access_token = token_info.get("access_token")
            
            # 使用 access token 獲取用戶信息
            user_response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if user_response.status_code != 200:
                return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?error=user_info_failed")
            
            user_info = user_response.json()
            
            # 生成簡單的用戶 token (實際應該使用 JWT)
            user_token = secrets.token_urlsafe(32)
            
            # 這裡應該將用戶信息保存到資料庫
            # 暫時返回成功頁面
            return RedirectResponse(
                url=f"{FRONTEND_URL}/auth/google/callback?login=success&token={user_token}&email={user_info.get('email')}&name={urllib.parse.quote(user_info.get('name', ''))}"
            )
            
    except Exception as e:
        return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?error=oauth_error&details={str(e)}")

@app.get("/api/auth/me")
async def get_current_user():
    """獲取當前用戶信息 (模擬端點)"""
    return {
        "message": "此端點需要實際的用戶認證系統",
        "status": "not_implemented"
    }

@app.post("/api/auth/logout")
async def logout():
    """用戶登出"""
    return {
        "message": "登出成功",
        "status": "logged_out"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
