# 🚀 Google Cloud Run 部署指南

## 📋 部署準備清單

### 1. 必需的文件已準備
- ✅ `Dockerfile` - Cloud Run 容器配置
- ✅ `cloudbuild.yaml` - 自動部署配置  
- ✅ `requirements-core.txt` - Python依賴
- ✅ `.gcloudignore` - 排除不需要的文件

### 2. Google Cloud 專案設置

#### 第一次設置（一次性）
```bash
# 設置專案ID（替換為您的專案ID）
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# 啟用必要的API
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# 創建 Artifact Registry（用於存儲Docker映像）
gcloud artifacts repositories create auto-trade-repo \
    --repository-format=docker \
    --location=asia-northeast1 \
    --description="AI Trading System Docker Repository"
```

## 🎯 快速部署方法

### 方法1: 直接部署（最簡單）
```bash
# 一鍵部署到 Cloud Run
gcloud run deploy auto-trade-ai \
    --source . \
    --region asia-northeast1 \
    --platform managed \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --timeout 900 \
    --set-env-vars "ENVIRONMENT=production,DEBUG=false"
```

### 方法2: 使用Cloud Build（CI/CD）
```bash
# 觸發 Cloud Build 自動部署
gcloud builds submit --config cloudbuild.yaml \
    --substitutions=_REGION=asia-northeast1,_AR_REPO=auto-trade-repo,_SERVICE=auto-trade-ai
```

## 🔧 環境變數設置

### 必需的環境變數
部署後需要設置：
```bash
# 設置 OpenAI API Key
gcloud run services update auto-trade-ai \
    --region asia-northeast1 \
    --set-env-vars "OPENAI_API_KEY=你的OpenAI_API_Key"

# 設置 Google OAuth（如果需要）
gcloud run services update auto-trade-ai \
    --region asia-northeast1 \
    --set-env-vars "GOOGLE_CLIENT_SECRET=你的Google_Client_Secret"
```

### 可選的環境變數
```bash
gcloud run services update auto-trade-ai \
    --region asia-northeast1 \
    --set-env-vars "JWT_SECRET_KEY=你的JWT密鑰,DATABASE_URL=sqlite:///tmp/trading.db"
```

## 📊 部署後驗證

### 1. 獲取服務URL
```bash
gcloud run services describe auto-trade-ai --region=asia-northeast1 --format='value(status.url)'
```

### 2. 測試API端點
```bash
# 健康檢查
curl https://your-service-url/health

# API文檔
open https://your-service-url/docs

# 股票分析
curl -X POST "https://your-service-url/analyze/AAPL" \
    -H "Content-Type: application/json" \
    -d '{"symbol": "AAPL", "period": "1mo"}'
```

## 🛡️ 安全設置

### 域名和HTTPS
Cloud Run 自動提供：
- ✅ HTTPS SSL證書
- ✅ 自動擴展
- ✅ 全球負載平衡

### 身份驗證（可選）
如需要身份驗證：
```bash
# 移除公開訪問
gcloud run services remove-iam-policy-binding auto-trade-ai \
    --region=asia-northeast1 \
    --member="allUsers" \
    --role="roles/run.invoker"
```

## 💰 成本估算

### Free Tier（每月免費）
- ✅ 2 million requests
- ✅ 400,000 GB-seconds
- ✅ 200,000 vCPU-seconds

### 估算月費（超出免費額度）
- **輕量使用**: $0-5/月
- **中等使用**: $10-30/月  
- **重度使用**: $50-100/月

## 🔄 CI/CD 自動部署

### GitHub Actions（推薦）
創建 `.github/workflows/deploy.yml`：
```yaml
name: Deploy to Cloud Run
on:
  push:
    branches: [ master ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - uses: google-github-actions/setup-gcloud@v0
      with:
        service_account_key: ${{ secrets.GCP_SA_KEY }}
        project_id: ${{ secrets.GCP_PROJECT_ID }}
        
    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy auto-trade-ai \
          --source . \
          --region asia-northeast1 \
          --allow-unauthenticated
```

## 🛠️ 常見問題解決

### 問題1: 部署超時
**解決**:
```bash
# 增加超時時間和資源
gcloud run deploy auto-trade-ai \
    --timeout 900 \
    --memory 2Gi \
    --cpu 2
```

### 問題2: 依賴安裝失敗
**解決**: 檢查 `requirements-core.txt` 是否包含所有必需依賴

### 問題3: 應用無法啟動
**解決**:
```bash
# 查看日誌
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=auto-trade-ai" --limit 50
```

## 🎉 部署成功！

部署完成後您將獲得：
- 🌐 HTTPS安全訪問URL
- 📊 自動縮放（0-100個實例）
- 💼 企業級可靠性
- 🔄 滾動更新和回滾
- 📈 內建監控和日誌

**您的AI交易系統現已部署在Google Cloud！** 🎊