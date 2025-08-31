#!/usr/bin/env python3
"""
Railway部署狀態檢查器
監控微服務部署進度和健康狀態
"""

import httpx
import time
import json
from datetime import datetime

class DeploymentChecker:
    """部署狀態檢查器"""
    
    def __init__(self):
        self.potential_urls = [
            "https://auto-trade-production.up.railway.app",
            "https://stock-helper-production.up.railway.app", 
            "https://capable-integrity-production.up.railway.app",
            "https://core-api-production.up.railway.app",
            "https://chart-service-production.up.railway.app"
        ]
        self.services = {
            "core": None,
            "chart": None
        }
    
    def check_url(self, url, service_type="unknown"):
        """檢查單個URL"""
        try:
            response = httpx.get(f"{url}/health", timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                return {
                    "url": url,
                    "status": "healthy",
                    "service": data.get("service", service_type),
                    "response_time": response.elapsed.total_seconds(),
                    "data": data
                }
            else:
                return {
                    "url": url,
                    "status": f"http_{response.status_code}",
                    "service": service_type
                }
        except httpx.ConnectError:
            return {
                "url": url,
                "status": "connection_failed",
                "service": service_type
            }
        except httpx.TimeoutException:
            return {
                "url": url,
                "status": "timeout",
                "service": service_type
            }
        except Exception as e:
            return {
                "url": url,
                "status": f"error: {str(e)}",
                "service": service_type
            }
    
    def check_root_endpoint(self, url):
        """檢查根端點以識別服務類型"""
        try:
            response = httpx.get(url, timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                service_name = data.get("service", "unknown")
                
                if "Core API" in service_name:
                    return "core"
                elif "Chart" in service_name:
                    return "chart"
            return "unknown"
        except:
            return "unknown"
    
    def discover_services(self):
        """發現可用的服務"""
        print("🔍 掃描Railway部署狀態...")
        print("-" * 50)
        
        found_services = []
        
        for url in self.potential_urls:
            print(f"檢查: {url}")
            
            # 先檢查根端點以識別服務類型
            service_type = self.check_root_endpoint(url)
            
            # 檢查健康狀態
            result = self.check_url(url, service_type)
            
            if result["status"] == "healthy":
                print(f"  ✅ 發現 {result['service']} - 響應時間: {result['response_time']:.3f}秒")
                found_services.append(result)
                
                # 記錄服務URL
                if "core" in result['service'].lower() or service_type == "core":
                    self.services["core"] = url
                elif "chart" in result['service'].lower() or service_type == "chart":
                    self.services["chart"] = url
                    
            elif result["status"].startswith("http_"):
                print(f"  ⚠️  響應但狀態異常: {result['status']}")
            else:
                print(f"  ❌ {result['status']}")
        
        return found_services
    
    def test_service_integration(self):
        """測試服務間集成"""
        print("\n🔄 測試服務集成...")
        
        if not self.services["core"]:
            print("  ❌ 核心服務未找到，無法測試集成")
            return False
            
        try:
            # 測試核心服務基本功能
            response = httpx.get(f"{self.services['core']}/symbols", timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ 核心服務股票代碼查詢正常 (總計: {data.get('total', 0)})")
            else:
                print(f"  ⚠️  核心服務響應異常: {response.status_code}")
                
            # 如果圖表服務可用，測試圖表生成
            if self.services["chart"]:
                chart_response = httpx.post(
                    f"{self.services['chart']}/generate-chart",
                    json={
                        "symbol": "DEPLOYMENT_TEST",
                        "chart_type": "basic",
                        "theme": "dark"
                    },
                    timeout=15.0
                )
                
                if chart_response.status_code == 200:
                    chart_data = chart_response.json()
                    if chart_data.get("success"):
                        print("  ✅ 圖表服務集成正常")
                    else:
                        print("  ⚠️  圖表服務響應但生成失敗")
                else:
                    print(f"  ⚠️  圖表服務響應異常: {chart_response.status_code}")
            else:
                print("  ⚠️  圖表服務未部署，跳過集成測試")
                
            return True
            
        except Exception as e:
            print(f"  ❌ 集成測試失敗: {str(e)}")
            return False
    
    def monitor_deployment(self, duration_minutes=10):
        """監控部署狀態"""
        print(f"\n⏱️  開始監控部署狀態 ({duration_minutes}分鐘)...")
        
        start_time = datetime.now()
        check_interval = 30  # 30秒檢查一次
        
        while (datetime.now() - start_time).total_seconds() < duration_minutes * 60:
            print(f"\n📊 {datetime.now().strftime('%H:%M:%S')} - 檢查部署狀態")
            
            services = self.discover_services()
            
            if len(services) >= 1:  # 至少有一個服務運行
                print("🎉 發現運行中的服務！")
                self.test_service_integration()
                
                if len(services) >= 2:
                    print("🚀 微服務架構部署成功！")
                    return True
                else:
                    print("⏳ 等待更多服務部署完成...")
            else:
                print("⏳ 等待服務部署...")
            
            print(f"下次檢查: {check_interval}秒後")
            time.sleep(check_interval)
        
        print(f"\n⏰ 監控超時 ({duration_minutes}分鐘)")
        return False
    
    def generate_deployment_report(self):
        """生成部署報告"""
        print("\n" + "="*60)
        print("📋 部署狀態報告")
        print("="*60)
        
        services = self.discover_services()
        
        if services:
            print(f"✅ 發現 {len(services)} 個運行中的服務:")
            for service in services:
                print(f"  • {service['service']}")
                print(f"    URL: {service['url']}")
                print(f"    響應時間: {service.get('response_time', 'N/A')}秒")
                
            print(f"\n🔗 服務URL:")
            if self.services["core"]:
                print(f"  核心服務: {self.services['core']}")
            if self.services["chart"]:
                print(f"  圖表服務: {self.services['chart']}")
                
        else:
            print("❌ 未發現運行中的服務")
            print("\n💡 可能的原因:")
            print("  • 部署仍在進行中")  
            print("  • Railway配置問題")
            print("  • Docker構建失敗")
            print("  • 環境變數缺失")

def main():
    """主函數"""
    checker = DeploymentChecker()
    
    print("🚀 Railway微服務部署監控器")
    print("="*60)
    
    # 立即檢查當前狀態
    services = checker.discover_services()
    
    if services:
        print(f"\n🎉 發現 {len(services)} 個服務正在運行！")
        checker.test_service_integration()
        
        if len(services) >= 2:
            print("\n✅ 微服務架構部署完成！")
        else:
            print("\n⏳ 部分服務仍在部署中...")
            checker.monitor_deployment(5)  # 監控5分鐘
    else:
        print("\n⏳ 未發現運行中的服務，開始監控...")
        checker.monitor_deployment(10)  # 監控10分鐘
    
    checker.generate_deployment_report()

if __name__ == "__main__":
    main()