const { chromium } = require('playwright');

async function debugRailwayService() {
    console.log('🔍 Debug Railway Service Configuration...');
    
    const browser = await chromium.launch({ 
        headless: false,
        slowMo: 500
    });
    
    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });
    
    const page = await context.newPage();
    
    try {
        const projectId = 'fe272568-e1ef-45ad-a5d2-a4674491fb8c';
        
        // 直接前往服務頁面
        console.log('🚀 Checking Railway service details...');
        await page.goto(`https://railway.com/project/${projectId}`);
        await page.waitForLoadState('networkidle');
        
        // 點擊服務
        console.log('📦 Clicking on service...');
        await page.click('text=stock_helper, text=auto_trade, [data-testid*="service"]'.split(', ')[0]);
        await page.waitForTimeout(3000);
        
        console.log('📸 Screenshot current service page...');
        await page.screenshot({ path: 'railway_service_debug.png', fullPage: true });
        
        // 檢查設置
        console.log('⚙️ Checking settings...');
        const settingsSelectors = [
            'text=Settings',
            'text=Configuration', 
            'text=Environment',
            'text=Variables'
        ];
        
        for (const selector of settingsSelectors) {
            try {
                if (await page.locator(selector).first().isVisible({ timeout: 2000 })) {
                    console.log(`⚙️ Found settings: ${selector}`);
                    await page.locator(selector).first().click();
                    await page.waitForTimeout(2000);
                    await page.screenshot({ path: 'railway_settings.png', fullPage: true });
                    break;
                }
            } catch (e) {
                console.log(`⏭️ Skip: ${selector}`);
            }
        }
        
        // 檢查日誌
        console.log('📋 Checking logs...');
        const logSelectors = [
            'text=Logs',
            'text=Deploy Logs',
            'text=Build Logs',
            'text=Runtime Logs'
        ];
        
        for (const selector of logSelectors) {
            try {
                if (await page.locator(selector).first().isVisible({ timeout: 2000 })) {
                    console.log(`📋 Found logs: ${selector}`);
                    await page.locator(selector).first().click();
                    await page.waitForTimeout(3000);
                    await page.screenshot({ path: 'railway_logs.png', fullPage: true });
                    break;
                }
            } catch (e) {
                console.log(`⏭️ Skip: ${selector}`);
            }
        }
        
        console.log('🎉 Debug screenshots taken!');
        console.log('📁 Check these files:');
        console.log('  - railway_service_debug.png');
        console.log('  - railway_settings.png (if found)');
        console.log('  - railway_logs.png (if found)');
        
    } catch (error) {
        console.error('❌ Debug error:', error.message);
        await page.screenshot({ path: 'railway_debug_error.png', fullPage: true });
    }
    
    console.log('Browser will close in 10 seconds...');
    await page.waitForTimeout(10000);
    await browser.close();
}

debugRailwayService().catch(console.error);