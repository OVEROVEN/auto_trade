#!/usr/bin/env python3
"""
使用Render API檢查部署狀態和日誌
"""
import requests
import json

def check_render_status():
    """檢查Render服務狀態和日誌"""
    
    api_key = "rnd_NB5KFN6sdsZxaC1gaaH2wcbAYRWS"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    print("🔍 Checking Render services...")
    
    try:
        # 獲取所有服務
        response = requests.get("https://api.render.com/v1/services", headers=headers)
        
        if response.status_code == 200:
            services = response.json()
            print(f"📊 Found {len(services)} services")
            
            for service in services:
                name = service.get("name", "Unknown")
                service_id = service.get("id", "Unknown")
                status = service.get("serviceDetails", {}).get("status", "Unknown")
                url = service.get("serviceDetails", {}).get("url", "No URL")
                
                print(f"\n🏷️ Service: {name}")
                print(f"🆔 ID: {service_id}")
                print(f"📊 Status: {status}")
                print(f"🌐 URL: {url}")
                
                # 如果是我們的服務，獲取詳細日誌
                if "auto-trade" in name.lower():
                    print(f"\n📋 Getting logs for {name}...")
                    
                    # 獲取部署日誌
                    logs_response = requests.get(
                        f"https://api.render.com/v1/services/{service_id}/deploys",
                        headers=headers
                    )
                    
                    if logs_response.status_code == 200:
                        deploys = logs_response.json()
                        if deploys:
                            latest_deploy = deploys[0]
                            deploy_id = latest_deploy.get("id")
                            deploy_status = latest_deploy.get("status")
                            
                            print(f"🚀 Latest deploy: {deploy_id}")
                            print(f"📊 Deploy status: {deploy_status}")
                            
                            # 獲取構建日誌
                            build_logs_response = requests.get(
                                f"https://api.render.com/v1/services/{service_id}/deploys/{deploy_id}/logs",
                                headers=headers
                            )
                            
                            if build_logs_response.status_code == 200:
                                logs_data = build_logs_response.json()
                                print(f"\n📝 Build Logs:")
                                print("-" * 50)
                                
                                for log_entry in logs_data[-10:]:  # 最後10條日誌
                                    timestamp = log_entry.get("timestamp", "")
                                    message = log_entry.get("message", "")
                                    print(f"[{timestamp}] {message}")
                            else:
                                print(f"❌ Failed to get logs: {build_logs_response.status_code}")
                    
                    # 檢查服務健康狀態
                    print(f"\n💓 Testing service health...")
                    if url and url != "No URL":
                        try:
                            health_response = requests.get(f"{url}/health", timeout=10)
                            print(f"🏥 Health check: {health_response.status_code}")
                            if health_response.status_code == 200:
                                print(f"✅ Response: {health_response.text[:200]}")
                            else:
                                print(f"❌ Health check failed: {health_response.text[:200]}")
                        except Exception as e:
                            print(f"❌ Health check error: {str(e)}")
                
        else:
            print(f"❌ Failed to get services: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ API Error: {str(e)}")

if __name__ == "__main__":
    print("🎯 Render Service Status Checker")
    print("=" * 50)
    check_render_status()