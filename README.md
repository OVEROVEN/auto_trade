# 🚀 AI Trading System - 完整部署指南

## 📋 項目簡介

AI Trading System 是一個專業的 AI 驱動股票分析平台，集成了技術分析、AI 建議、多市場支援（美股 + 台股）和 Google OAuth 認證。

### ✨ 核心功能
- 🤖 **AI 分析**：基於 GPT-4o 的智能投資建議
- 📊 **技術指標**：RSI、MACD、移動平均線等 15+ 指標
- 🔍 **形態識別**：自動識別頭肩頂、雙重頂底等經典形態
- 🌍 **多市場**：支援美股 (AAPL, GOOGL) 和台股 (2330.TW)
- 🔐 **安全認證**：Google OAuth + JWT token 系統
- 📈 **視覺化**：K線圖表 + 技術指標圖表
- 💳 **配額系統**：用戶使用配額和兌換碼功能

## 🛠️ 快速開始

### 步驟 1: 環境準備

```bash
# 克隆項目
git clone <your-repo-url>
cd auto_trade

# 安裝依賴
pip install -r requirements-core.txt

# 或使用 Google Cloud 優化版本
pip install -r requirements-gcloud.txt
```

### 步驟 2: 環境變數配置

```bash
# 複製環境變數範本
cp .env.example .env

# 編輯 .env 檔案，填入您的實際配置
nano .env
```

### 步驟 3: 配置驗證

```bash
# 檢查配置是否正確
python test_config.py

# 應該看到類似輸出：
# ✅ OpenAI API configured: True
# ✅ Google OAuth configured: True
```

### 步驟 4: 啟動應用

```bash
# 啟動後端服務
python main_integrated.py

# 後端將運行在: http://localhost:8080
# API 文檔: http://localhost:8080/docs
```

### 步驟 5: 啟動前端 (可選)

```bash
# 進入前端目錄
cd frontend

# 安裝依賴
npm install

# 啟動前端
npm run dev

# 前端將運行在: http://localhost:3000
```

## 🔧 環境變數配置詳解

### 📋 **必填配置**

#### 🤖 OpenAI API (AI 功能)
```bash
# 從 https://platform.openai.com/ 獲取
OPENAI_API_KEY=sk-proj-your-openai-api-key-here
```

#### 🔐 JWT 認證
```bash
# 生成強隨機字串
# python -c "import secrets; print(secrets.token_urlsafe(32))"
JWT_SECRET=your-secure-jwt-secret-here
```

#### 🌐 Google OAuth (社交登入)
```bash
# 從 https://console.developers.google.com/ 獲取
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 📋 **可選配置**

#### 🗄️ 資料庫
```bash
# 預設使用 SQLite (適合開發/小型部署)
DATABASE_URL=sqlite:///./trading.db

# 生產環境建議使用 PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost:5432/trading_db
```

#### 🌐 服務設定
```bash
PORT=8080
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 🔍 配置檢查工具

使用內建工具驗證配置：

```bash
python test_config.py
```

**輸出範例：**
```
🔧 AI Trading System - 配置檢查工具
==================================================
✅ 統一配置模塊已載入

📊 服務狀態:

🔹 Openai:
  ✅ configured: True
  📋 model: gpt-4o
  📋 api_key_preview: sk-proj-...

🔹 Google_oauth:
  ✅ configured: True
  📋 client_id_preview: 1234567890...

🔍 配置驗證:
✅ 所有關鍵配置都正確
```

## ☁️ 部署指南

### 🌟 本地開發
```bash
# 使用統一的啟動腳本
python main_integrated.py

# 或使用 uvicorn (更多控制)
uvicorn main_integrated:app --host 0.0.0.0 --port 8080 --reload
```

### 🐳 Docker 部署
```bash
# 使用 Docker Compose (推薦)
docker-compose up -d

# 或手動建置
docker build -f Dockerfile.integrated -t ai-trading-system .
docker run -p 8080:8080 --env-file .env ai-trading-system
```

### ☁️ Google Cloud Run 部署

#### 前置準備
```bash
# 1. 啟用必要服務
gcloud services enable run.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com

# 2. 創建 Artifact Registry
gcloud artifacts repositories create ai-trading-repo \
    --repository-format=docker \
    --location=asia-northeast1

# 3. 設置 Secret Manager
echo "your-openai-api-key" | gcloud secrets create openai-api-key --data-file=-
echo "your-jwt-secret" | gcloud secrets create jwt-secret --data-file=-
```

#### 自動部署
```bash
# 使用 Cloud Build 自動部署
gcloud builds submit --config cloudbuild-backend.yaml
```

#### 手動部署
```bash
# 建置映像
docker build -f Dockerfile.cloudrun.fixed -t gcr.io/YOUR_PROJECT_ID/ai-trading-backend .

# 推送映像
docker push gcr.io/YOUR_PROJECT_ID/ai-trading-backend

# 部署到 Cloud Run
gcloud run deploy ai-trading-system-backend \
    --image gcr.io/YOUR_PROJECT_ID/ai-trading-backend \
    --region asia-northeast1 \
    --platform managed \
    --allow-unauthenticated \
    --set-secrets "OPENAI_API_KEY=openai-api-key:latest,JWT_SECRET=jwt-secret:latest"
```

### 🚂 Railway 部署
```bash
# 1. 安裝 Railway CLI
npm install -g @railway/cli

# 2. 登入並初始化
railway login
railway init

# 3. 設置環境變數
railway variables set OPENAI_API_KEY=your-key
railway variables set GOOGLE_CLIENT_ID=your-id
railway variables set JWT_SECRET=your-secret

# 4. 部署
railway up
```

### ⚡ Render 部署
1. 連接 GitHub repository
2. 選擇 Web Service
3. 設置環境變數：
   - `OPENAI_API_KEY`
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`
   - `JWT_SECRET`
4. 使用 `requirements-core.txt`
5. 啟動命令：`python main_integrated.py`

## 📖 API 使用指南

### 🔍 健康檢查
```bash
curl http://localhost:8080/health
```

### 📊 股票分析
```bash
# 基礎分析
curl -X POST "http://localhost:8080/analyze/AAPL" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "include_ai": false}'

# AI 增強分析 (需要認證)
curl -X POST "http://localhost:8080/analyze/AAPL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"symbol": "AAPL", "include_ai": true}'
```

### 🔐 Google OAuth 登入流程
1. 訪問：`http://localhost:8080/api/auth/google`
2. 完成 Google 認證
3. 獲得 JWT token
4. 使用 token 訪問受保護的 API

### 📈 支援的股票代碼
- **美股**：AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA
- **台股**：2330.TW (台積電), 2317.TW (鴻海) 等

## 🔧 開發指南

### 📁 項目結構
```
auto_trade/
├── main_integrated.py          # 主應用程式
├── config/
│   ├── __init__.py
│   └── api_config.py          # 統一配置管理
├── frontend/                  # 前端應用 (Next.js)
├── .env.example              # 環境變數範本
├── requirements-core.txt     # 核心依賴
├── requirements-gcloud.txt   # Google Cloud 優化依賴
├── test_config.py           # 配置驗證工具
├── Dockerfile.cloudrun.fixed # Google Cloud Run Dockerfile
├── cloudbuild-backend.yaml  # Cloud Build 配置
└── README.md               # 本檔案
```

### 🧪 測試
```bash
# 配置測試
python test_config.py

# API 測試
curl http://localhost:8080/docs  # Swagger UI

# 功能測試
python -c "
from config import get_openai_client, is_openai_configured
if is_openai_configured():
    client = get_openai_client()
    print('✅ OpenAI client 設定成功')
else:
    print('❌ OpenAI 未設定')
"
```

### 📊 監控和日誌
```bash
# 查看應用日誌
tail -f logs/trading.log

# Google Cloud Run 日誌
gcloud run services logs read ai-trading-system-backend --region asia-northeast1

# 健康檢查
curl http://localhost:8080/health
```

## ❓ 常見問題

### Q: AI 功能不可用？
A: 檢查 `OPENAI_API_KEY` 是否正確設置：
```bash
python test_config.py
# 應該顯示: ✅ OpenAI API configured: True
```

### Q: Google 登入失敗？
A: 確認以下設定：
1. `GOOGLE_CLIENT_ID` 和 `GOOGLE_CLIENT_SECRET` 正確
2. Google Console 中已添加正確的 redirect URI
3. OAuth consent screen 已設定

### Q: 圖表顯示亂碼？
A: 系統已自動配置中文字體支援，如仍有問題請檢查系統字體安裝。

### Q: 部署到雲端後無法訪問？
A: 檢查：
1. 環境變數是否正確設置在雲端平台
2. 端口配置 (預設 8080)
3. CORS 設定是否包含前端域名

## 📞 技術支援

- 📖 **完整文檔**：查看項目內的各種 `.md` 檔案
- 🔧 **配置問題**：執行 `python test_config.py`
- 🐛 **問題回報**：請提供詳細的錯誤訊息和配置狀態
- 💬 **功能建議**：歡迎提出改進建議

## 📄 授權

本項目採用 MIT 授權條款。

---

**🎉 享受 AI 驅動的智能交易分析！**