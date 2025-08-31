const { chromium } = require('playwright');

async function automateRailwayDeployment() {
    console.log('🚀 啟動Railway自動部署...');
    
    const browser = await chromium.launch({ 
        headless: false, // 顯示瀏覽器窗口，你可以看到操作過程
        slowMo: 1000 // 放慢操作速度，便於觀察
    });
    
    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });
    
    const page = await context.newPage();
    
    try {
        // 步驟 1: 前往Railway登入頁面
        console.log('📝 前往Railway登入頁面...');
        await page.goto('https://railway.app/login');
        await page.waitForLoadState('networkidle');
        
        // 檢查是否已經登入
        const isLoggedIn = await page.locator('text=Dashboard').isVisible().catch(() => false);
        
        if (!isLoggedIn) {
            console.log('🔐 需要登入Railway...');
            console.log('請在瀏覽器中手動完成登入，然後按任意鍵繼續...');
            
            // 等待用戶手動登入
            await page.waitForURL('**/dashboard**', { timeout: 300000 }); // 等待5分鐘
            console.log('✅ 登入成功！');
        }
        
        // 步驟 2: 前往項目頁面
        console.log('📁 尋找stock_helper項目...');
        await page.goto('https://railway.app/dashboard');
        await page.waitForLoadState('networkidle');
        
        // 尋找stock_helper項目
        const projectSelector = 'text=stock_helper';
        await page.waitForSelector(projectSelector, { timeout: 10000 });
        await page.click(projectSelector);
        
        console.log('✅ 找到stock_helper項目');
        
        // 步驟 3: 配置GitHub集成
        console.log('🔗 設置GitHub集成...');
        await page.waitForLoadState('networkidle');
        
        // 尋找設置或部署按鈕
        const settingsSelector = 'text=Settings, text=Deploy, text=Connect Repo, [data-testid="deploy-button"]';
        
        // 嘗試多種可能的按鈕
        const buttons = [
            'text=Deploy',
            'text=Connect Repository', 
            'text=Connect Repo',
            'text=GitHub',
            'button:has-text("Deploy")',
            '[data-testid*="deploy"]',
            '[data-testid*="github"]'
        ];
        
        let buttonFound = false;
        for (const buttonSelector of buttons) {
            const button = await page.locator(buttonSelector).first();
            if (await button.isVisible().catch(() => false)) {
                console.log(`🎯 找到按鈕: ${buttonSelector}`);
                await button.click();
                buttonFound = true;
                break;
            }
        }
        
        if (!buttonFound) {
            console.log('📸 截圖當前頁面以便分析...');
            await page.screenshot({ path: 'railway-dashboard.png', fullPage: true });
            console.log('💡 請檢查railway-dashboard.png截圖，手動點擊部署相關按鈕');
            
            // 等待用戶手動操作
            console.log('請手動點擊部署或GitHub連接按鈕，然後按Enter繼續...');
            process.stdin.setRawMode(true);
            process.stdin.resume();
            await new Promise(resolve => process.stdin.once('data', resolve));
            process.stdin.setRawMode(false);
        }
        
        // 步驟 4: 連接GitHub倉庫
        console.log('📦 連接GitHub倉庫...');
        await page.waitForTimeout(2000);
        
        // 尋找GitHub倉庫選項
        const repoSelector = 'text=OVEROVEN/auto_trade, text=auto_trade';
        const repoElement = await page.locator(repoSelector).first();
        
        if (await repoElement.isVisible().catch(() => false)) {
            await repoElement.click();
            console.log('✅ 已選擇auto_trade倉庫');
        } else {
            console.log('🔍 截圖以查找倉庫選項...');
            await page.screenshot({ path: 'railway-repo-selection.png', fullPage: true });
        }
        
        // 步驟 5: 配置構建設置
        console.log('⚙️ 配置構建設置...');
        await page.waitForTimeout(2000);
        
        // 尋找Dockerfile配置
        const dockerfileInputs = [
            'input[placeholder*="Dockerfile"]',
            'input[value*="Dockerfile"]',
            'text=Dockerfile.core'
        ];
        
        for (const selector of dockerfileInputs) {
            const input = await page.locator(selector).first();
            if (await input.isVisible().catch(() => false)) {
                await input.clear();
                await input.fill('Dockerfile.core');
                console.log('✅ 設置Dockerfile路徑為Dockerfile.core');
                break;
            }
        }
        
        // 步驟 6: 觸發部署
        console.log('🚀 觸發部署...');
        const deployButtons = [
            'text=Deploy',
            'text=Deploy Now', 
            'button:has-text("Deploy")',
            '[data-testid*="deploy"]'
        ];
        
        for (const buttonSelector of deployButtons) {
            const button = await page.locator(buttonSelector).first();
            if (await button.isVisible().catch(() => false)) {
                await button.click();
                console.log('✅ 部署已觸發！');
                break;
            }
        }
        
        // 步驟 7: 監控部署進度
        console.log('📊 監控部署進度...');
        await page.waitForTimeout(5000);
        
        // 截圖最終狀態
        await page.screenshot({ path: 'railway-deployment-status.png', fullPage: true });
        console.log('📸 已截圖部署狀態');
        
        // 等待部署完成或顯示進度
        const maxWaitTime = 10 * 60 * 1000; // 10分鐘
        const startTime = Date.now();
        
        while (Date.now() - startTime < maxWaitTime) {
            const statusElements = await page.locator('text=Building, text=Deploying, text=Success, text=Failed, text=Running').all();
            
            if (statusElements.length > 0) {
                const statusText = await statusElements[0].textContent();
                console.log(`📈 部署狀態: ${statusText}`);
                
                if (statusText?.includes('Success') || statusText?.includes('Running')) {
                    console.log('🎉 部署成功！');
                    break;
                } else if (statusText?.includes('Failed')) {
                    console.log('❌ 部署失敗，請檢查日誌');
                    break;
                }
            }
            
            await page.waitForTimeout(10000); // 等待10秒
        }
        
        console.log('✅ Railway自動化操作完成！');
        
    } catch (error) {
        console.error('❌ 自動化過程中出現錯誤:', error);
        await page.screenshot({ path: 'railway-error.png', fullPage: true });
        console.log('📸 已截圖錯誤頁面: railway-error.png');
    }
    
    console.log('瀏覽器將保持開啟，你可以手動檢查結果...');
    console.log('按任意鍵關閉瀏覽器...');
    
    // 等待用戶輸入後關閉瀏覽器
    process.stdin.setRawMode(true);
    process.stdin.resume();
    await new Promise(resolve => process.stdin.once('data', resolve));
    process.stdin.setRawMode(false);
    
    await browser.close();
}

// 運行自動化腳本
automateRailwayDeployment().catch(console.error);