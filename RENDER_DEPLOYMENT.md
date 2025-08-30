# 🚀 Render 部署指南

## 部署步驟

### 1. 準備工作
- 確保您有 Render 帳號：https://render.com
- 將程式碼推送到 GitHub 存儲庫

### 2. 創建 Render 服務

#### 方法 A：使用 Blueprint (推薦)
1. 在 Render Dashboard 中點擊 "New +"
2. 選擇 "Blueprint"
3. 連接您的 GitHub 存儲庫
4. Render 會自動偵測 `render.yaml` 並建立服務

#### 方法 B：手動建立 Web Service
1. 在 Render Dashboard 中點擊 "New +"
2. 選擇 "Web Service"
3. 連接您的 GitHub 存儲庫
4. 配置設定：
   - **Name**: ai-trading-system
   - **Runtime**: Docker
   - **Build Command**: (留空，由 Dockerfile 處理)
   - **Start Command**: `./render-start.sh`
   - **Plan**: Free (或升級為付費方案以獲得更好效能)

### 3. 環境變數設定

在 Render Dashboard 中設定以下環境變數：

#### 必需的環境變數：
```bash
ENVIRONMENT=production
DEBUG=false
PORT=10000  # Render 會自動設定
OPENAI_API_KEY=your_actual_openai_api_key_here
DATABASE_URL=sqlite:///./data/trading.db
DATABASE_PASSWORD=your_secure_password
API_HOST=0.0.0.0
```

#### 可選的環境變數：
```bash
# AI 模型配置
AI_MODEL_BASIC=gpt-3.5-turbo
AI_MODEL_ADVANCED=gpt-4o-mini
AI_MODEL_VISION=gpt-4o
AI_AUTO_MODEL_SELECTION=true
AI_MAX_TOKENS=2000
AI_TEMPERATURE=0.7

# 資料庫配置（如升級到 PostgreSQL）
# DATABASE_URL=postgresql://user:pass@host:port/db

# Redis 配置（可選）
# REDIS_URL=redis://localhost:6379/0
```

### 4. 部署過程

1. **自動建置**：Render 會自動運行 Docker 建置
2. **部署時間**：首次部署約需 5-10 分鐘
3. **健康檢查**：系統會自動檢查 `/health` 端點
4. **啟動完成**：您會收到部署完成的通知

### 5. 訪問您的應用程式

部署完成後，您會獲得一個 URL，例如：
```
https://ai-trading-system-xyz.onrender.com
```

可用的端點：
- **首頁**: https://your-app.onrender.com/
- **API 文檔**: https://your-app.onrender.com/docs
- **健康檢查**: https://your-app.onrender.com/health

## 🔧 疑難排解

### 部署失敗
1. 檢查 Render 的建置日誌
2. 確認所有環境變數都已設定
3. 驗證 Dockerfile 語法正確

### 應用程式無法啟動
1. 檢查 `render-start.sh` 腳本權限
2. 確認 PORT 環境變數正確設定
3. 查看應用程式日誌

### 效能問題
1. 考慮升級到付費方案
2. 啟用持久磁碟存儲
3. 配置適當的資源限制

## 📊 監控和維護

### 日誌監控
- 在 Render Dashboard 中查看即時日誌
- 設定日誌警報

### 效能監控
- 使用 Render 內建的效能指標
- 監控 API 響應時間
- 設定健康檢查警報

### 自動更新
- 連接 GitHub 存儲庫自動部署
- 設定分支保護規則
- 使用 GitHub Actions 進行 CI/CD

## 💰 成本估算

### Free Plan
- **限制**: 750 小時/月、512MB RAM、0.1 CPU
- **適合**: 開發和測試
- **成本**: 免費

### Starter Plan ($7/月)
- **包含**: 無限小時、512MB RAM、0.5 CPU
- **適合**: 輕量生產環境
- **成本**: $7/月

### Standard Plan ($25/月)
- **包含**: 無限小時、2GB RAM、1 CPU
- **適合**: 標準生產環境
- **成本**: $25/月

## 🚀 優化建議

### 效能優化
1. 啟用 Redis 快取
2. 設定適當的數據庫連接池
3. 使用 CDN 加速靜態資源

### 安全性優化
1. 設定適當的 CORS 政策
2. 使用 HTTPS（Render 自動提供）
3. 定期更新依賴項

### 監控優化
1. 整合第三方監控服務
2. 設定錯誤追蹤
3. 配置效能分析

---

🎉 **恭喜！您的 AI 交易系統現在可以在雲端運行了！**