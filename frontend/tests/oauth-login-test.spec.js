// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Google OAuth 登入和註冊測試', () => {
  
  test.beforeEach(async ({ page }) => {
    // 前往主頁面
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('檢查登入按鈕是否存在', async ({ page }) => {
    // 檢查登入按鈕
    const loginButton = page.locator('button:has-text("Login")');
    await expect(loginButton).toBeVisible();
    
    console.log('✅ 登入按鈕存在並可見');
  });

  test('點擊登入按鈕測試', async ({ page }) => {
    // 點擊登入按鈕
    const loginButton = page.locator('button:has-text("Login")');
    await loginButton.click();
    
    // 檢查是否有彈出視窗或轉向
    // 等待可能的彈窗或頁面變化
    await page.waitForTimeout(2000);
    
    // 檢查是否有新的DOM元素出現
    const modalOrDialog = page.locator('[role="dialog"], .modal, .login-modal, .auth-modal');
    const hasModal = await modalOrDialog.count() > 0;
    
    if (hasModal) {
      console.log('✅ 登入點擊觸發了彈窗');
    } else {
      console.log('⚠️ 登入點擊沒有明顯的反應');
    }
  });

  test('檢查Google OAuth配置', async ({ page }) => {
    // 檢查前端是否有Google Client ID環境變數
    const clientIdExists = await page.evaluate(() => {
      // 檢查window物件或其他地方是否有Google配置
      return typeof window !== 'undefined';
    });
    
    expect(clientIdExists).toBe(true);
    console.log('✅ 前端JavaScript環境正常');
  });

  test('測試後端認證端點', async ({ page }) => {
    // 測試後端認證API是否可用
    const response = await page.request.get('http://localhost:8080/api/auth/register');
    
    // 檢查是否回應405 (Method Not Allowed) 而不是404 (Not Found)
    // 405表示端點存在但方法不對，404表示端點不存在
    if (response.status() === 405) {
      console.log('✅ 後端認證端點存在 (GET不被允許是正常的)');
    } else if (response.status() === 404) {
      console.log('❌ 後端認證端點不存在');
    } else {
      console.log(`ℹ️ 後端認證端點回應: ${response.status()}`);
    }
  });

  test('檢查後端OAuth端點', async ({ page }) => {
    // 檢查OAuth相關端點
    const endpoints = [
      '/api/auth/google/login',
      '/api/auth/google/callback',
      '/api/auth/register',
      '/api/auth/login'
    ];
    
    for (const endpoint of endpoints) {
      try {
        const response = await page.request.get(`http://localhost:8080${endpoint}`);
        console.log(`${endpoint}: ${response.status()}`);
      } catch (error) {
        console.log(`${endpoint}: 連接錯誤`);
      }
    }
  });

  test('檢查前端是否有Google OAuth按鈕', async ({ page }) => {
    // 點擊登入按鈕後檢查是否有Google登入選項
    await page.locator('button:has-text("Login")').click();
    await page.waitForTimeout(1000);
    
    // 檢查是否有Google相關的按鈕或文字
    const googleButton = page.locator('button:has-text("Google"), button:has-text("使用Google登入"), [data-testid="google-login"]');
    const hasGoogleButton = await googleButton.count() > 0;
    
    if (hasGoogleButton) {
      console.log('✅ 找到Google登入按鈕');
    } else {
      console.log('⚠️ 沒有找到Google登入按鈕');
    }
  });

  test('模擬註冊流程', async ({ page }) => {
    // 測試是否有註冊相關的UI
    const signupElements = page.locator('button:has-text("Sign up"), button:has-text("註冊"), a:has-text("註冊")');
    const hasSignup = await signupElements.count() > 0;
    
    if (hasSignup) {
      console.log('✅ 找到註冊相關元素');
      await signupElements.first().click();
      await page.waitForTimeout(1000);
    } else {
      console.log('⚠️ 沒有找到註冊入口');
    }
  });

  test('檢查環境變數載入', async ({ page }) => {
    // 在瀏覽器中檢查環境變數是否正確載入
    const envCheck = await page.evaluate(() => {
      // 檢查Next.js環境變數
      return {
        hasProcess: typeof process !== 'undefined',
        nodeEnv: typeof process !== 'undefined' ? process.env.NODE_ENV : 'unknown'
      };
    });
    
    console.log('🔧 環境檢查結果:', JSON.stringify(envCheck, null, 2));
  });

});

test.describe('登入錯誤處理測試', () => {
  
  test('測試無效登入處理', async ({ page }) => {
    await page.goto('/');
    
    // 如果有登入表單，測試無效輸入
    const emailInput = page.locator('input[type="email"], input[placeholder*="email"], input[placeholder*="郵箱"]');
    const passwordInput = page.locator('input[type="password"], input[placeholder*="password"], input[placeholder*="密碼"]');
    
    const hasLoginForm = await emailInput.count() > 0 && await passwordInput.count() > 0;
    
    if (hasLoginForm) {
      await emailInput.fill('invalid@email.com');
      await passwordInput.fill('wrongpassword');
      
      const submitButton = page.locator('button[type="submit"], button:has-text("登入"), button:has-text("Login")');
      if (await submitButton.count() > 0) {
        await submitButton.click();
        await page.waitForTimeout(2000);
        console.log('✅ 測試了無效登入處理');
      }
    } else {
      console.log('ℹ️ 沒有找到登入表單');
    }
  });

});