# 🚀 GitHub自動部署到Railway指南

## 📋 設置步驟

### 1. Railway項目設置
1. 登入 [Railway](https://railway.app)
2. 在你的 `stock_helper` 項目中點擊 "Settings"
3. 選擇 "Integrations" → "GitHub"
4. 連接你的 GitHub 倉庫 `OVEROVEN/auto_trade`

### 2. 獲取Railway令牌
1. 在Railway項目設置中，找到 "Tokens"
2. 創建一個新的項目令牌
3. 複製令牌值（格式：`rnd_xxxxx...`）

### 3. 設置GitHub Secrets
1. 打開 [GitHub倉庫設置](https://github.com/OVEROVEN/auto_trade/settings)
2. 選擇 "Security" → "Secrets and variables" → "Actions"
3. 添加以下secrets：

| Secret名稱 | 值 | 說明 |
|-----------|---|------|
| `RAILWAY_TOKEN` | `rnd_xxxxx...` | Railway項目令牌 |
| `RAILWAY_SERVICE_ID` | `auto_trade` | Railway服務ID |

### 4. 配置Railway服務設置
在Railway項目中設置以下環境變數：

```
ENVIRONMENT=production
DEBUG=false
SERVICE_NAME=core-api
OPENAI_API_KEY=你的OpenAI密鑰
GOOGLE_CLIENT_SECRET=你的Google密鑰
DATABASE_URL=sqlite:///./data/trading.db
GOOGLE_CLIENT_ID=610357573971-t2r6c0b3i8fq8kng1j8e5s4l6jiqiggf.apps.googleusercontent.com
```

### 5. 部署配置確認
確保以下文件在倉庫根目錄：
- ✅ `railway.toml` - Railway配置
- ✅ `Dockerfile.core` - Docker構建文件  
- ✅ `requirements-core.txt` - Python依賴
- ✅ `.railwayignore` - 排除不必要文件
- ✅ `.github/workflows/railway-deploy.yml` - GitHub Actions

## 🔄 自動部署流程

### 觸發條件
- 推送到 `master` 或 `main` 分支
- 創建Pull Request

### 部署步驟
1. **代碼檢出** - GitHub Actions檢出最新代碼
2. **安裝Railway CLI** - 安裝部署工具
3. **執行部署** - 使用Railway CLI部署服務
4. **健康檢查** - 驗證部署是否成功

### 監控部署
1. 打開 [GitHub Actions](https://github.com/OVEROVEN/auto_trade/actions)
2. 查看 "Deploy to Railway" 工作流程
3. 監控部署日誌和狀態

## 🎯 部署URL

部署成功後，服務將可通過以下URL訪問：
- **核心服務**: https://stock-helper-production.up.railway.app
- **健康檢查**: https://stock-helper-production.up.railway.app/health
- **API文檔**: https://stock-helper-production.up.railway.app/docs

## 🛠️ 故障排除

### 問題1：部署失敗 - "Unauthorized"
**解決方案**：
- 檢查 `RAILWAY_TOKEN` secret是否正確設置
- 確認令牌沒有過期

### 問題2：服務無法啟動
**解決方案**：
- 檢查Railway項目的環境變數
- 查看Railway部署日誌
- 確認 `Dockerfile.core` 配置正確

### 問題3：健康檢查失敗
**解決方案**：
- 等待更長時間（第一次部署可能需要3-5分鐘）
- 檢查Railway服務狀態
- 驗證 `/health` 端點是否正確實現

## 📊 手動觸發部署

如需手動觸發部署：
1. 進入 [GitHub Actions](https://github.com/OVEROVEN/auto_trade/actions)
2. 選擇 "Deploy to Railway" 工作流程
3. 點擊 "Run workflow"
4. 選擇分支並執行

## 🎉 部署驗證

部署完成後驗證：
```bash
# 健康檢查
curl https://stock-helper-production.up.railway.app/health

# API端點測試  
curl https://stock-helper-production.up.railway.app/symbols

# 打開API文檔
open https://stock-helper-production.up.railway.app/docs
```

## 🚀 下一步

1. **設置自動部署** - 按照上述步驟配置
2. **推送代碼觸發** - 任何推送都會自動部署
3. **監控部署狀態** - 通過GitHub Actions監控
4. **配置圖表服務** - 重複流程部署圖表微服務

---

**🎯 GitHub + Railway = 無縫自動化部署！**