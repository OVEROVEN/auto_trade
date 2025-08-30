#!/bin/bash

# AI Trading Dashboard 綜合測試腳本
echo "🚀 AI Trading Dashboard 綜合測試開始..."
echo "========================================"

# 建立測試結果目錄
mkdir -p test-results
mkdir -p screenshots

# 顏色定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}步驟 1: 檢查服務狀態${NC}"
echo "----------------------------------------"

# 檢查 Next.js 服務
echo "檢查 Next.js 服務 (localhost:3000)..."
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Next.js 服務運行正常${NC}"
else
    echo -e "${RED}✗ Next.js 服務未運行，請先啟動: npm run dev${NC}"
    exit 1
fi

# 檢查後端 API 服務
echo "檢查後端 API 服務 (localhost:8000)..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ API 服務運行正常${NC}"
else
    echo -e "${YELLOW}⚠ API 服務未運行，某些測試可能失敗${NC}"
fi

echo -e "\n${YELLOW}步驟 2: 安裝測試依賴${NC}"
echo "----------------------------------------"
if [ ! -d "node_modules/@playwright" ]; then
    echo "安裝 Playwright..."
    npm install @playwright/test
    npx playwright install
else
    echo -e "${GREEN}✓ Playwright 已安裝${NC}"
fi

echo -e "\n${YELLOW}步驟 3: 執行綜合測試${NC}"
echo "----------------------------------------"

# 執行測試
echo "開始執行 Playwright 測試..."
npx playwright test --reporter=html,line

TEST_EXIT_CODE=$?

echo -e "\n${YELLOW}步驟 4: 生成測試報告${NC}"
echo "----------------------------------------"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ 所有測試通過！${NC}"
else
    echo -e "${RED}❌ 部分測試失敗，請查看詳細報告${NC}"
fi

# 創建測試摘要
cat > test-results/test-summary.md << EOF
# AI Trading Dashboard 測試報告

## 測試執行時間
**執行日期:** $(date)
**測試狀態:** $([ $TEST_EXIT_CODE -eq 0 ] && echo "✅ 通過" || echo "❌ 失敗")

## 測試項目覆蓋

### 1. 頁面基本載入和響應 ✓
- 頁面標題驗證
- 主要元素載入檢查
- 狀態指示器驗證

### 2. 股票搜尋功能 ✓
- AAPL 搜尋測試
- TSLA 搜尋測試  
- 2330.TW 搜尋測試
- 載入狀態驗證

### 3. 流行股票按鈕功能 ✓
- 按鈕點擊響應
- 狀態變更驗證
- 圖表更新檢查

### 4. 圖表載入狀態 ✓
- 載入指示器檢查
- TradingView 整合驗證
- 圖表工具列測試

### 5. AI分析面板 ✓
- AI 分析觸發
- 載入狀態檢查
- 結果顯示驗證

### 6. 市場數據顯示 ✓
- 實時數據顯示
- 數據項目驗證
- 狀態更新檢查

### 7. 技術分析功能卡片 ✓
- 功能卡片顯示
- 狀態指示器
- 互動效果測試

### 8. 系統狀態指示器 ✓
- API 連接狀態
- 實時數據狀態
- 系統時間顯示

### 9. 響應式設計測試 ✓
- 桌面視窗 (1920x1080)
- 平板視窗 (768x1024)  
- 手機視窗 (375x667)

### 10. 錯誤檢測和API連接 ✓
- JavaScript 錯誤監控
- API 連接測試
- 錯誤處理驗證

### 11. 性能測試 ✓
- 頁面載入時間測量
- 搜尋響應時間測量
- 網絡請求分析

## 截圖文件
測試過程中自動生成的截圖保存在 \`test-results/\` 目錄中：

$(ls -la test-results/*.png 2>/dev/null | awk '{print "- " $9}' || echo "- 無截圖文件生成")

## 建議改進項目
1. 加強錯誤處理機制
2. 優化載入性能
3. 增加更多用戶互動回饋
4. 改善移動端體驗

---
*本報告由自動化測試工具生成*
EOF

echo -e "\n${YELLOW}步驟 5: 開啟測試報告${NC}"
echo "----------------------------------------"
echo "測試報告已生成："
echo "- HTML 報告: playwright-report/index.html"
echo "- 測試摘要: test-results/test-summary.md"
echo "- 截圖文件: test-results/*.png"

# 嘗試打開 HTML 報告
if command -v open &> /dev/null; then
    echo "正在打開測試報告..."
    open playwright-report/index.html
elif command -v xdg-open &> /dev/null; then
    xdg-open playwright-report/index.html
else
    echo "請手動打開 playwright-report/index.html 查看詳細報告"
fi

echo -e "\n${GREEN}測試執行完成！${NC}"
echo "========================================"

exit $TEST_EXIT_CODE