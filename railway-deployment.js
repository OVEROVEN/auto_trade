const { chromium } = require('playwright');

async function deployToRailway() {
    console.log('🚀 啟動Railway部署自動化...');
    
    const browser = await chromium.launch({ 
        headless: false,
        slowMo: 500
    });
    
    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });
    
    const page = await context.newPage();
    
    try {
        console.log('📱 前往Railway Dashboard...');
        await page.goto('https://railway.app/dashboard');
        await page.waitForLoadState('networkidle');
        
        console.log('🎯 點擊stock_helper項目...');
        await page.click('text=stock_helper');
        await page.waitForLoadState('networkidle');
        
        console.log('📸 截圖項目頁面...');
        await page.screenshot({ path: 'stock_helper_project.png', fullPage: true });
        
        console.log('🔍 尋找服務...');
        await page.waitForTimeout(2000);
        
        // 尋找並點擊現有的服務
        const serviceElements = [
            '[data-testid*="service"]',
            '.service-card',
            'div:has-text("auto_trade")',
            'button:has-text("auto_trade")',
            'text=auto_trade'
        ];
        
        let serviceFound = false;
        for (const selector of serviceElements) {
            try {
                const element = await page.locator(selector).first();
                if (await element.isVisible({ timeout: 2000 })) {
                    console.log(`✅ 找到服務: ${selector}`);
                    await element.click();
                    serviceFound = true;
                    break;
                }
            } catch (e) {
                console.log(`⏭️  跳過選擇器: ${selector}`);
            }
        }
        
        if (!serviceFound) {
            console.log('🔗 嘗試創建新部署...');
            const deployButtons = [
                'text=Deploy from GitHub',
                'text=Deploy',
                'button:has-text("Deploy")',
                'text=Connect Repo',
                'text=New Service'
            ];
            
            for (const buttonSelector of deployButtons) {
                try {
                    const button = await page.locator(buttonSelector).first();
                    if (await button.isVisible({ timeout: 2000 })) {
                        console.log(`🎯 點擊部署按鈕: ${buttonSelector}`);
                        await button.click();
                        break;
                    }
                } catch (e) {
                    console.log(`⏭️  跳過按鈕: ${buttonSelector}`);
                }
            }
        }
        
        await page.waitForTimeout(3000);
        console.log('📸 截圖當前狀態...');
        await page.screenshot({ path: 'railway_service_page.png', fullPage: true });
        
        // 尋找設置或配置選項
        console.log('⚙️ 尋找設置選項...');
        const settingsElements = [
            'text=Settings',
            'text=Variables', 
            'text=Deploy',
            '[data-testid*="settings"]',
            'button:has-text("Settings")'
        ];
        
        for (const selector of settingsElements) {
            try {
                const element = await page.locator(selector).first();
                if (await element.isVisible({ timeout: 2000 })) {
                    console.log(`⚙️  找到設置: ${selector}`);
                    await element.click();
                    await page.waitForTimeout(2000);
                    break;
                }
            } catch (e) {
                console.log(`⏭️  跳過設置: ${selector}`);
            }
        }
        
        // 如果找到源代碼設置
        console.log('📦 配置GitHub源代碼...');
        const repoElements = [
            'text=OVEROVEN/auto_trade',
            'text=auto_trade',
            'input[placeholder*="repo"]',
            'text=Connect Repository'
        ];
        
        for (const selector of repoElements) {
            try {
                const element = await page.locator(selector).first();
                if (await element.isVisible({ timeout: 2000 })) {
                    console.log(`📦 處理倉庫: ${selector}`);
                    await element.click();
                    await page.waitForTimeout(2000);
                    break;
                }
            } catch (e) {
                console.log(`⏭️  跳過倉庫選項: ${selector}`);
            }
        }
        
        // 配置構建設置
        console.log('🏗️  配置構建設置...');
        const buildElements = [
            'input[placeholder*="Dockerfile"]',
            'text=Dockerfile',
            'input[value*="Dockerfile"]'
        ];
        
        for (const selector of buildElements) {
            try {
                const input = await page.locator(selector).first();
                if (await input.isVisible({ timeout: 2000 })) {
                    console.log('🔧 設置Dockerfile路徑...');
                    await input.clear();
                    await input.fill('Dockerfile.core');
                    console.log('✅ Dockerfile路徑已設置為Dockerfile.core');
                    break;
                }
            } catch (e) {
                console.log(`⏭️  跳過Dockerfile設置: ${selector}`);
            }
        }
        
        // 觸發部署
        console.log('🚀 觸發部署...');
        const finalDeployButtons = [
            'text=Deploy Now',
            'text=Redeploy', 
            'text=Deploy',
            'button:has-text("Deploy")',
            '[data-testid*="deploy"]'
        ];
        
        for (const buttonSelector of finalDeployButtons) {
            try {
                const button = await page.locator(buttonSelector).first();
                if (await button.isVisible({ timeout: 2000 })) {
                    console.log(`🚀 點擊部署: ${buttonSelector}`);
                    await button.click();
                    console.log('✅ 部署已觸發！');
                    await page.waitForTimeout(3000);
                    break;
                }
            } catch (e) {
                console.log(`⏭️  跳過部署按鈕: ${selector}`);
            }
        }
        
        console.log('📸 截圖最終狀態...');
        await page.screenshot({ path: 'railway_final_state.png', fullPage: true });
        
        console.log('📊 等待部署狀態更新...');
        await page.waitForTimeout(10000);
        
        // 檢查部署狀態
        const statusElements = await page.locator('text=/Building|Deploying|Success|Failed|Running|Live/').all();
        if (statusElements.length > 0) {
            const status = await statusElements[0].textContent();
            console.log(`📈 部署狀態: ${status}`);
        }
        
        console.log('📸 截圖部署結果...');
        await page.screenshot({ path: 'railway_deployment_result.png', fullPage: true });
        
        console.log('🎉 Railway部署自動化完成！');
        console.log('📁 生成的截圖文件：');
        console.log('  - stock_helper_project.png');
        console.log('  - railway_service_page.png');
        console.log('  - railway_final_state.png');
        console.log('  - railway_deployment_result.png');
        
    } catch (error) {
        console.error('❌ 自動化錯誤:', error.message);
        await page.screenshot({ path: 'railway_automation_error.png', fullPage: true });
    }
    
    console.log('瀏覽器將在10秒後關閉...');
    await page.waitForTimeout(10000);
    await browser.close();
}

deployToRailway().catch(console.error);