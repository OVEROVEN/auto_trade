const { chromium } = require('playwright');

async function directRailwayDeploy() {
    console.log('🎯 直接導航到Railway項目...');
    
    const browser = await chromium.launch({ 
        headless: false,
        slowMo: 300
    });
    
    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });
    
    const page = await context.newPage();
    
    try {
        // 從錯誤日誌中提取的項目ID
        const projectId = 'fe272568-e1ef-45ad-a5d2-a4674491fb8c';
        
        console.log('🚀 直接前往stock_helper項目頁面...');
        await page.goto(`https://railway.com/project/${projectId}`);
        await page.waitForLoadState('networkidle');
        
        console.log('📸 截圖項目內部頁面...');
        await page.screenshot({ path: 'railway_project_inside.png', fullPage: true });
        
        console.log('🔍 尋找現有服務...');
        
        // 等待頁面加載並尋找服務
        await page.waitForTimeout(3000);
        
        // 尋找auto_trade服務
        const serviceSelectors = [
            'text=auto_trade',
            'text=auto-trade',
            '[data-testid*="service"]',
            '.service',
            'div:has-text("auto_trade")',
            'div:has-text("auto-trade")'
        ];
        
        let serviceClicked = false;
        for (const selector of serviceSelectors) {
            try {
                const element = await page.locator(selector).first();
                if (await element.isVisible({ timeout: 3000 })) {
                    console.log(`✅ 找到並點擊服務: ${selector}`);
                    await element.click();
                    serviceClicked = true;
                    break;
                }
            } catch (e) {
                console.log(`⏭️  跳過服務選擇器: ${selector}`);
            }
        }
        
        if (!serviceClicked) {
            console.log('➕ 沒找到現有服務，嘗試創建新的...');
            
            const newServiceSelectors = [
                'text=New',
                'text=Add Service',
                'text=Deploy from GitHub',
                'button:has-text("New")',
                'button:has-text("Add")',
                '[data-testid*="new-service"]'
            ];
            
            for (const selector of newServiceSelectors) {
                try {
                    const element = await page.locator(selector).first();
                    if (await element.isVisible({ timeout: 2000 })) {
                        console.log(`➕ 點擊新建服務: ${selector}`);
                        await element.click();
                        await page.waitForTimeout(2000);
                        break;
                    }
                } catch (e) {
                    console.log(`⏭️  跳過新建按鈕: ${selector}`);
                }
            }
        }
        
        await page.waitForTimeout(3000);
        console.log('📸 截圖服務配置頁面...');
        await page.screenshot({ path: 'railway_service_config.png', fullPage: true });
        
        // 尋找GitHub倉庫配置
        console.log('📦 配置GitHub倉庫...');
        
        const repoSelectors = [
            'text=OVEROVEN/auto_trade',
            'input[placeholder*="repository"]',
            'input[placeholder*="repo"]',
            'text=Connect Repository',
            'text=auto_trade'
        ];
        
        for (const selector of repoSelectors) {
            try {
                const element = await page.locator(selector).first();
                if (await element.isVisible({ timeout: 3000 })) {
                    console.log(`📦 處理倉庫配置: ${selector}`);
                    await element.click();
                    await page.waitForTimeout(2000);
                    break;
                }
            } catch (e) {
                console.log(`⏭️  跳過倉庫選擇器: ${selector}`);
            }
        }
        
        // 如果需要選擇分支
        console.log('🌿 檢查分支設置...');
        const branchSelectors = [
            'text=master',
            'text=main',
            'select[name*="branch"]',
            'input[value="master"]',
            'input[value="main"]'
        ];
        
        for (const selector of branchSelectors) {
            try {
                const element = await page.locator(selector).first();
                if (await element.isVisible({ timeout: 2000 })) {
                    console.log(`🌿 設置分支: ${selector}`);
                    await element.click();
                    break;
                }
            } catch (e) {
                console.log(`⏭️  跳過分支選擇器: ${selector}`);
            }
        }
        
        // 設置根目錄（如果需要）
        console.log('📁 檢查根目錄設置...');
        const rootDirInputs = await page.locator('input[placeholder*="Root Directory"], input[name*="root"], input[label*="Root"]').all();
        
        for (const input of rootDirInputs) {
            try {
                if (await input.isVisible({ timeout: 1000 })) {
                    const currentValue = await input.inputValue();
                    if (!currentValue || currentValue === '/') {
                        console.log('📁 設置根目錄為當前目錄');
                        await input.fill('./');
                    }
                    break;
                }
            } catch (e) {
                console.log('⏭️  跳過根目錄設置');
            }
        }
        
        // 設置Dockerfile
        console.log('🐳 配置Dockerfile...');
        const dockerfileInputs = [
            'input[placeholder*="Dockerfile"]',
            'input[name*="dockerfile"]',
            'input[label*="Dockerfile"]'
        ];
        
        for (const selector of dockerfileInputs) {
            try {
                const input = await page.locator(selector).first();
                if (await input.isVisible({ timeout: 2000 })) {
                    console.log('🐳 設置Dockerfile路徑...');
                    await input.clear();
                    await input.fill('Dockerfile.core');
                    console.log('✅ Dockerfile設置為Dockerfile.core');
                    break;
                }
            } catch (e) {
                console.log(`⏭️  跳過Dockerfile設置: ${selector}`);
            }
        }
        
        await page.waitForTimeout(2000);
        console.log('📸 截圖配置完成狀態...');
        await page.screenshot({ path: 'railway_config_complete.png', fullPage: true });
        
        // 觸發部署
        console.log('🚀 觸發部署...');
        const deploySelectors = [
            'button:has-text("Deploy")',
            'text=Deploy Now',
            'text=Deploy',
            'button[type="submit"]',
            '[data-testid*="deploy"]'
        ];
        
        let deployTriggered = false;
        for (const selector of deploySelectors) {
            try {
                const button = await page.locator(selector).first();
                if (await button.isVisible({ timeout: 3000 })) {
                    console.log(`🚀 點擊部署按鈕: ${selector}`);
                    await button.click();
                    deployTriggered = true;
                    console.log('✅ 部署已觸發！');
                    break;
                }
            } catch (e) {
                console.log(`⏭️  跳過部署按鈕: ${selector}`);
            }
        }
        
        if (!deployTriggered) {
            console.log('🔄 嘗試按Enter鍵觸發部署...');
            await page.keyboard.press('Enter');
        }
        
        // 等待部署開始
        console.log('⏳ 等待部署開始...');
        await page.waitForTimeout(5000);
        
        console.log('📸 截圖部署狀態...');
        await page.screenshot({ path: 'railway_deployment_triggered.png', fullPage: true });
        
        // 監控部署狀態
        console.log('📊 監控部署狀態...');
        for (let i = 0; i < 6; i++) { // 最多監控1分鐘
            await page.waitForTimeout(10000); // 每10秒檢查一次
            
            const statusElements = await page.locator('text=/Building|Deploying|Success|Failed|Running|Live|Crashed/i').all();
            
            if (statusElements.length > 0) {
                const status = await statusElements[0].textContent();
                console.log(`📈 部署狀態 (${i+1}/6): ${status}`);
                
                if (status?.match(/Success|Running|Live/i)) {
                    console.log('🎉 部署成功！');
                    break;
                } else if (status?.match(/Failed|Crashed/i)) {
                    console.log('❌ 部署失敗');
                    break;
                }
            } else {
                console.log(`⏳ 檢查中... (${i+1}/6)`);
            }
        }
        
        console.log('📸 截圖最終狀態...');
        await page.screenshot({ path: 'railway_final_result.png', fullPage: true });
        
        console.log('🎉 Railway直接部署完成！');
        console.log('📁 生成的截圖：');
        console.log('  - railway_project_inside.png');
        console.log('  - railway_service_config.png');
        console.log('  - railway_config_complete.png');
        console.log('  - railway_deployment_triggered.png');
        console.log('  - railway_final_result.png');
        
    } catch (error) {
        console.error('❌ 部署錯誤:', error.message);
        await page.screenshot({ path: 'railway_direct_error.png', fullPage: true });
    }
    
    console.log('瀏覽器將在15秒後關閉，你可以手動檢查結果...');
    await page.waitForTimeout(15000);
    await browser.close();
}

directRailwayDeploy().catch(console.error);