# 🚀 Google Cloud Shell 一鍵部署命令

## ⚡ 立即執行 - 複製貼上即可

### 步驟1: 打開Google Cloud Shell
1. 前往：https://console.cloud.google.com
2. 點擊右上角的 `>_` 圖標 (Activate Cloud Shell)
3. 等待Shell啟動

### 步驟2: 複製貼上以下命令執行

```bash
# 設置專案ID
export PROJECT_ID="ai-trading-system-470613"
gcloud config set project $PROJECT_ID

# 啟用必要API
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# 下載代碼
git clone https://github.com/OVEROVEN/auto_trade.git
cd auto_trade

# 創建Cloud Run優化的Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴文件
COPY requirements-core.txt .

# 安裝Python依賴
RUN pip install --no-cache-dir -r requirements-core.txt

# 複製應用代碼
COPY src/ ./src/
COPY config/ ./config/

# 設置環境變數
ENV PYTHONPATH=/app
ENV ENVIRONMENT=production
ENV DEBUG=false
ENV DATABASE_URL=sqlite:///tmp/trading.db

# Cloud Run會自動設置$PORT環境變數
ENV PORT=8000
EXPOSE $PORT

# 啟動命令
CMD python -m uvicorn src.api.main:app --host 0.0.0.0 --port $PORT --workers 1
EOF

# 一鍵部署到Cloud Run
gcloud run deploy auto-trade-ai \
    --source . \
    --region asia-northeast1 \
    --platform managed \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --timeout 900 \
    --set-env-vars "ENVIRONMENT=production,DEBUG=false,DATABASE_URL=sqlite:///tmp/trading.db"

echo ""
echo "🎉 部署完成！"
echo "正在獲取服務URL..."

# 獲取服務URL
SERVICE_URL=$(gcloud run services describe auto-trade-ai --region=asia-northeast1 --format='value(status.url)')

echo ""
echo "🌐 您的AI交易系統已成功部署："
echo "服務URL: $SERVICE_URL"
echo "API文檔: $SERVICE_URL/docs"
echo "健康檢查: $SERVICE_URL/health"
echo "兌換碼API: $SERVICE_URL/api/redemption"
echo ""

# 測試健康檢查
echo "🧪 測試服務..."
curl -s "$SERVICE_URL/health" && echo "✅ 服務正常運行！" || echo "⚠️ 服務可能還在啟動中"
```

## 🎯 執行結果

執行完成後您會看到：

```
🎉 部署完成！
🌐 您的AI交易系統已成功部署：
服務URL: https://auto-trade-ai-xxx-an.a.run.app
API文檔: https://auto-trade-ai-xxx-an.a.run.app/docs
健康檢查: https://auto-trade-ai-xxx-an.a.run.app/health
兌換碼API: https://auto-trade-ai-xxx-an.a.run.app/api/redemption
✅ 服務正常運行！
```

## 📋 執行步驟總結

1. **打開Cloud Shell** (1分鐘)
2. **複製貼上上面的完整命令** (1分鐘)  
3. **等待部署完成** (3-5分鐘)
4. **獲得完整的服務URL** ✅

**總時間：約5-7分鐘**

## 🔧 可選：設置AI功能

如果需要AI分析功能，在Cloud Shell中執行：

```bash
gcloud run services update auto-trade-ai \
  --region asia-northeast1 \
  --set-env-vars "OPENAI_API_KEY=您的OpenAI金鑰"
```

## 🎊 準備好了嗎？

1. 打開 https://console.cloud.google.com
2. 啟動 Cloud Shell (點擊右上角 `>_`)
3. 複製貼上上面的完整命令
4. 等待部署完成！

**您的AI交易系統即將在Google Cloud Run上運行！** 🚀