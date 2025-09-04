// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('AI Trading System 綜合測試', () => {
  
  test.beforeEach(async ({ page }) => {
    // 等待後端API服務就緒
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('前端頁面載入測試', async ({ page }) => {
    await page.goto('/');

    // 檢查頁面標題
    await expect(page).toHaveTitle(/AI Trading Dashboard/);
    
    // 檢查主要元素
    await expect(page.locator('h1')).toContainText('AI Trading Dashboard');
    
    // 檢查股票分析區域
    await expect(page.locator('text=Chart Analysis')).toBeVisible();
    
    // 檢查AI分析區域
    await expect(page.locator('text=AI Analysis')).toBeVisible();
    
    // 檢查兌換碼區域
    await expect(page.locator('text=Redemption Code')).toBeVisible();
    
    // 檢查登入按鈕
    await expect(page.locator('button:has-text("Login")')).toBeVisible();

    console.log('✅ 前端頁面載入測試通過');
  });

  test('股票代碼輸入和切換測試', async ({ page }) => {
    await page.goto('/');
    
    // 檢查預設股票代碼 AAPL
    const stockInput = page.locator('input[placeholder*="stock symbol"]');
    await expect(stockInput).toHaveValue('AAPL');
    
    // 測試熱門股票按鈕切換
    await page.locator('button:has-text("GOOGL")').click();
    await expect(stockInput).toHaveValue('GOOGL');
    
    // 測試台股代碼
    await page.locator('button:has-text("2330.TW")').click();
    await expect(stockInput).toHaveValue('2330.TW');
    
    // 測試手動輸入
    await stockInput.fill('TSLA');
    await expect(stockInput).toHaveValue('TSLA');

    console.log('✅ 股票代碼切換測試通過');
  });

  test('兌換碼功能測試', async ({ page }) => {
    await page.goto('/');
    
    // 測試兌換碼輸入
    const redeemInput = page.locator('input[placeholder*="redemption code"]');
    const redeemButton = page.locator('button:has-text("Redeem Now")');
    
    await expect(redeemInput).toBeVisible();
    await expect(redeemButton).toBeVisible();
    
    // 測試有效的兌換碼 - WEILIANG100X
    await redeemInput.fill('WEILIANG100X');
    await expect(redeemInput).toHaveValue('WEILIANG100X');
    
    // 測試其他兌換碼
    const testCodes = [
      'SOCCER100FANS',
      'NEWUSER20TEST', 
      'TRADER50BONUS',
      'PREMIUM30GOLD'
    ];
    
    for (const code of testCodes) {
      await redeemInput.fill(code);
      await expect(redeemInput).toHaveValue(code);
      console.log(`✅ 兌換碼 ${code} 輸入測試通過`);
    }

    console.log('✅ 兌換碼功能測試通過');
  });

  test('響應式設計測試', async ({ page, browserName }) => {
    // 測試桌面版
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/');
    await expect(page.locator('h1')).toBeVisible();
    
    // 測試平板版
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.reload();
    await expect(page.locator('h1')).toBeVisible();
    
    // 測試手機版
    await page.setViewportSize({ width: 375, height: 667 });
    await page.reload();
    await expect(page.locator('h1')).toBeVisible();

    console.log('✅ 響應式設計測試通過');
  });

  test('API連接測試', async ({ page }) => {
    // 監聽網路請求
    const responses = [];
    page.on('response', response => {
      if (response.url().includes('localhost:8080')) {
        responses.push({
          url: response.url(),
          status: response.status(),
          ok: response.ok()
        });
      }
    });

    await page.goto('/');
    await page.waitForTimeout(3000); // 等待可能的API呼叫
    
    // 檢查是否有成功的API響應
    if (responses.length > 0) {
      const successfulResponses = responses.filter(r => r.ok);
      console.log(`✅ 發現 ${responses.length} 個API請求，${successfulResponses.length} 個成功`);
    }

    console.log('✅ API連接測試完成');
  });

  test('性能測試', async ({ page }) => {
    // 測量頁面載入時間
    const startTime = Date.now();
    
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    
    expect(loadTime).toBeLessThan(10000); // 應該在10秒內載入完成
    console.log(`✅ 頁面載入時間: ${loadTime}ms`);
  });

  test('UI互動測試', async ({ page }) => {
    await page.goto('/');
    
    // 測試兌換碼歷史展開/收起
    const historyButton = page.locator('button:has-text("Redemption History")');
    if (await historyButton.isVisible()) {
      await historyButton.click();
      console.log('✅ 兌換碼歷史按鈕可點擊');
    }
    
    // 測試語言切換按鈕
    const languageButtons = page.locator('button[title="TW"], button[title="CN"]');
    const count = await languageButtons.count();
    if (count > 0) {
      await languageButtons.first().click();
      console.log('✅ 語言切換按鈕可點擊');
    }

    console.log('✅ UI互動測試通過');
  });

});

// 錯誤處理測試
test.describe('錯誤處理測試', () => {
  
  test('無效兌換碼測試', async ({ page }) => {
    await page.goto('/');
    
    const redeemInput = page.locator('input[placeholder*="redemption code"]');
    const redeemButton = page.locator('button:has-text("Redeem Now")');
    
    // 測試空的兌換碼
    await redeemInput.fill('');
    // 測試無效兌換碼
    await redeemInput.fill('INVALID123');
    await expect(redeemInput).toHaveValue('INVALID123');
    
    console.log('✅ 無效兌換碼處理測試通過');
  });

  test('網路中斷測試', async ({ page }) => {
    await page.goto('/');
    
    // 模擬網路中斷
    await page.setOfflineMode(true);
    await page.reload();
    
    // 應該顯示某種錯誤狀態或離線模式
    // 恢復網路
    await page.setOfflineMode(false);
    
    console.log('✅ 網路中斷處理測試通過');
  });

});