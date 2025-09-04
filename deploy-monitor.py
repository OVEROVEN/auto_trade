#!/usr/bin/env python3
"""
Railway部署監控腳本
檢查部署狀態並測試服務健康
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime

# 部署URL
RAILWAY_URL = "https://autotrade-production-a264.up.railway.app"

async def check_service_health(session, url, timeout=10):
    """檢查服務健康狀態"""
    try:
        async with session.get(f"{url}/health", timeout=timeout) as response:
            if response.status == 200:
                data = await response.json()
                return True, data
            else:
                return False, f"HTTP {response.status}"
    except asyncio.TimeoutError:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

async def check_api_endpoints(session, url):
    """檢查關鍵API端點"""
    endpoints = [
        ("/", "根路徑"),
        ("/health", "健康檢查"),
        ("/symbols", "股票代碼"),
        ("/docs", "API文檔")
    ]
    
    results = {}
    
    for endpoint, description in endpoints:
        try:
            async with session.get(f"{url}{endpoint}", timeout=10) as response:
                results[endpoint] = {
                    "description": description,
                    "status": response.status,
                    "success": response.status == 200
                }
        except Exception as e:
            results[endpoint] = {
                "description": description,
                "status": "error",
                "success": False,
                "error": str(e)
            }
    
    return results

async def test_redemption_api(session, url):
    """測試兌換碼API（不需要認證的端點）"""
    try:
        # 測試兌換碼創建端點（通常需要管理員權限，這裡只測試連接）
        async with session.get(f"{url}/api/redemption/admin/codes", timeout=10) as response:
            return {
                "endpoint": "/api/redemption/admin/codes",
                "status": response.status,
                "accessible": response.status in [200, 401, 403]  # 200=成功, 401/403=需要認證（正常）
            }
    except Exception as e:
        return {
            "endpoint": "/api/redemption/admin/codes", 
            "status": "error",
            "accessible": False,
            "error": str(e)
        }

async def monitor_deployment():
    """監控部署狀態"""
    print("🚀 Railway部署監控開始")
    print(f"📍 目標URL: {RAILWAY_URL}")
    print("=" * 60)
    
    max_attempts = 30  # 最多嘗試30次（約15分鐘）
    attempt = 0
    
    async with aiohttp.ClientSession() as session:
        while attempt < max_attempts:
            attempt += 1
            current_time = datetime.now().strftime("%H:%M:%S")
            
            print(f"\n🔍 第 {attempt} 次檢查 ({current_time})")
            
            # 檢查基本健康狀態
            is_healthy, health_data = await check_service_health(session, RAILWAY_URL)
            
            if is_healthy:
                print("✅ 服務健康檢查通過")
                print(f"   服務狀態: {health_data.get('status', 'unknown')}")
                print(f"   服務名稱: {health_data.get('service', 'unknown')}")
                
                # 檢查API端點
                print("\n📊 檢查API端點...")
                endpoint_results = await check_api_endpoints(session, RAILWAY_URL)
                
                all_endpoints_ok = True
                for endpoint, result in endpoint_results.items():
                    status = "✅" if result['success'] else "❌"
                    print(f"   {status} {endpoint}: {result['description']} (HTTP {result['status']})")
                    if not result['success']:
                        all_endpoints_ok = False
                
                # 檢查兌換碼API
                print("\n🎫 檢查兌換碼API...")
                redemption_result = await test_redemption_api(session, RAILWAY_URL)
                redemption_status = "✅" if redemption_result['accessible'] else "❌"
                print(f"   {redemption_status} 兌換碼API: HTTP {redemption_result['status']}")
                
                if all_endpoints_ok and redemption_result['accessible']:
                    print(f"\n🎊 部署成功！")
                    print(f"🌐 服務URL: {RAILWAY_URL}")
                    print(f"📚 API文檔: {RAILWAY_URL}/docs")
                    print(f"🔍 健康檢查: {RAILWAY_URL}/health")
                    
                    # 保存部署結果
                    deployment_result = {
                        "success": True,
                        "url": RAILWAY_URL,
                        "timestamp": datetime.now().isoformat(),
                        "health_check": health_data,
                        "endpoints": endpoint_results,
                        "redemption_api": redemption_result,
                        "attempts": attempt
                    }
                    
                    with open('deployment-result.json', 'w', encoding='utf-8') as f:
                        json.dump(deployment_result, f, ensure_ascii=False, indent=2)
                    
                    print(f"✅ 部署結果已保存到 deployment-result.json")
                    return True
                else:
                    print(f"⚠️ 部分端點未就緒，繼續等待...")
            else:
                print(f"❌ 服務尚未就緒: {health_data}")
            
            if attempt < max_attempts:
                print(f"⏳ 等待30秒後重新檢查...")
                await asyncio.sleep(30)
            
        print(f"\n⚠️ 監控超時，已嘗試 {max_attempts} 次")
        print(f"🔗 請手動檢查: {RAILWAY_URL}")
        return False

async def main():
    """主函數"""
    try:
        success = await monitor_deployment()
        if success:
            print("\n🎯 部署監控完成 - 成功")
        else:
            print("\n⚠️ 部署監控完成 - 需要手動檢查")
    except KeyboardInterrupt:
        print("\n\n⏹️ 監控被用戶中斷")
    except Exception as e:
        print(f"\n❌ 監控出現錯誤: {e}")

if __name__ == "__main__":
    asyncio.run(main())