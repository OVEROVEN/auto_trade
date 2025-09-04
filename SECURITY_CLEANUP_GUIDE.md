# 🚨 GitHub 上傳前安全清理指南

## ⚠️ **重要警告：當前代碼包含敏感資訊，不能直接上傳！**

### 🔍 **發現的安全問題**：

#### 1. **敏感憑證暴露**
```bash
# Google OAuth Client ID (多處暴露)
your-google-client-id.apps.googleusercontent.com

# JWT Secret Keys (完整暴露)
your-jwt-secret-key-here

# 硬編碼 JWT Tokens (可被破解)
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.your-test-token-content-here...
```

#### 2. **包含敏感資訊的檔案**
- `frontend/.env.local` - 完整憑證
- `cloudbuild.yaml` - 實際 Google Client ID
- `cloudbuild-backend.yaml` - JWT 金鑰
- `browser_test_script.js` - 測試 token
- `test_jwt_redemption.js` - JWT token
- `create_jwt_token.py` - 測試憑證
- `railway.toml` - 部分憑證

## 🛠️ **必須執行的清理步驟**

### 步驟 1: 使用安全版本的 .gitignore
```bash
# 替換為安全版本
cp .gitignore.secure .gitignore
```

### 步驟 2: 刪除包含敏感資訊的檔案
```bash
# 刪除包含真實憑證的檔案
rm -f frontend/.env.local
rm -f cloudbuild.yaml
rm -f cloudbuild-backend.yaml
rm -f railway.toml
rm -f browser_test_script.js
rm -f test_jwt_redemption.js
rm -f create_jwt_token.py
rm -f create_test_user.py

# 刪除包含實際憑證的部署指南
rm -f *DEPLOYMENT*.md
rm -f *deployment*.md
rm -f gcloud-deploy-guide.md
```

### 步驟 3: 清理代碼中的硬編碼憑證
```python
# main_integrated.py 中需要修改的部分：
# 移除任何硬編碼的 API keys, secrets, tokens
# 確保所有敏感資訊都從環境變數讀取
```

### 步驟 4: 創建安全的範本檔案
```bash
# 使用已創建的安全範本
cp .env.example .env.template
```

### 步驟 5: 檢查並清理所有 YAML 配置檔案
```bash
# 檢查所有配置檔案，確保不包含真實憑證
grep -r "your-google-client" . --exclude-dir=.git || echo "✅ Google Client ID 已清理"
grep -r "your-jwt-secret" . --exclude-dir=.git || echo "✅ JWT Secret 已清理"
grep -r "eyJhbGciOiJIUzI1NiI" . --exclude-dir=.git || echo "✅ JWT Token 已清理"
```

## 📋 **安全上傳檢查清單**

### ✅ 必須完成的項目：
- [ ] 使用 `.gitignore.secure` 取代原始 `.gitignore`
- [ ] 刪除所有包含真實憑證的檔案
- [ ] 驗證 `main_integrated.py` 不包含硬編碼憑證
- [ ] 創建 `.env.example` 範本檔案
- [ ] 移除所有測試用 JWT tokens
- [ ] 清理部署配置檔案中的實際憑證
- [ ] 檢查所有 markdown 檔案中的憑證範例
- [ ] 確認沒有資料庫檔案被包含

### 🔍 **上傳前最終檢查**：
```bash
# 搜尋可能遺漏的敏感資訊
grep -r -i "sk-" . --exclude-dir=.git --exclude-dir=node_modules
grep -r -i "secret" . --exclude-dir=.git --exclude-dir=node_modules | grep -v "example"
grep -r -i "token" . --exclude-dir=.git --exclude-dir=node_modules | grep -v "example"
grep -r -i "key" . --exclude-dir=.git --exclude-dir=node_modules | grep -v "example"
grep -r -i "password" . --exclude-dir=.git --exclude-dir=node_modules | grep -v "example"
```

## 🚀 **安全的部署策略**

### 1. **環境變數管理**
- 使用 `.env.example` 作為範本
- 在部署平台設置實際環境變數
- 絕不在代碼中硬編碼憑證

### 2. **CI/CD 最佳實踐**
- 使用 GitHub Secrets 存儲敏感資訊
- 使用 Secret Manager (GCP) 或類似服務
- 在建置時動態注入憑證

### 3. **開發團隊協作**
- 每個開發者維護自己的 `.env` 檔案
- 共享 `.env.example` 範本
- 定期輪換生產環境憑證

## 🔐 **重新生成所有憑證**

### 上傳到 GitHub 前必須重新生成：
1. **JWT Secret**: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
2. **Google OAuth**: 在 Google Console 重新生成 Client ID/Secret
3. **OpenAI API Key**: 檢查是否需要輪換

## ⚠️ **緊急情況處理**

### 如果意外上傳了敏感資訊：
1. **立即撤銷**所有暴露的 API keys
2. **重新生成**所有憑證
3. **清理 Git 歷史** (如果已提交)
4. **通知團隊**更新憑證

### Git 歷史清理 (如果需要)：
```bash
# 移除敏感檔案的完整歷史
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch frontend/.env.local' \
  --prune-empty --tag-name-filter cat -- --all

# 強制推送清理後的歷史 (危險操作！)
git push --force --all
```

## ✅ **清理完成後可以安全上傳**

完成所有清理步驟後，您的項目將可以安全地上傳到公開的 GitHub repository，同時保護所有敏感資訊。

---

**記住：安全是第一優先！寧可多花時間檢查，也不要冒洩露風險。** 🛡️