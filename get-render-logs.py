#!/usr/bin/env python3
"""
獲取auto-trade-core的部署日誌
"""
import requests
import json

def get_deploy_logs():
    api_key = "rnd_NB5KFN6sdsZxaC1gaaH2wcbAYRWS"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # auto-trade-core服務ID
    service_id = "srv-d2q76dje5dus73bo3hb0"
    
    print("🚀 Getting deployment logs for auto-trade-core...")
    print(f"🆔 Service ID: {service_id}")
    print(f"🌐 Service URL: https://auto-trade-core.onrender.com")
    
    try:
        # 獲取部署列表
        print("\n📋 Getting deployments...")
        deploys_response = requests.get(
            f"https://api.render.com/v1/services/{service_id}/deploys",
            headers=headers
        )
        
        if deploys_response.status_code == 200:
            deploys = deploys_response.json()
            if deploys:
                latest_deploy = deploys[0]
                deploy_id = latest_deploy.get("id")
                deploy_status = latest_deploy.get("status")
                created_at = latest_deploy.get("createdAt")
                finished_at = latest_deploy.get("finishedAt")
                
                print(f"🚀 Latest Deploy ID: {deploy_id}")
                print(f"📊 Status: {deploy_status}")
                print(f"⏰ Created: {created_at}")
                print(f"🏁 Finished: {finished_at}")
                
                # 獲取詳細日誌
                print(f"\n📝 Getting detailed logs...")
                logs_response = requests.get(
                    f"https://api.render.com/v1/services/{service_id}/deploys/{deploy_id}/logs",
                    headers=headers
                )
                
                if logs_response.status_code == 200:
                    logs = logs_response.json()
                    print(f"\n📄 Deploy Logs ({len(logs)} entries):")
                    print("=" * 80)
                    
                    for log_entry in logs[-30:]:  # 最後30條日誌
                        timestamp = log_entry.get("timestamp", "")
                        message = log_entry.get("message", "")
                        level = log_entry.get("level", "")
                        print(f"[{timestamp[:19]}] {level} {message}")
                    
                else:
                    print(f"❌ Failed to get logs: {logs_response.status_code}")
                    print(f"Response: {logs_response.text}")
            else:
                print("📭 No deployments found")
        else:
            print(f"❌ Failed to get deploys: {deploys_response.status_code}")
            print(f"Response: {deploys_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🎯 Auto-Trade-Core Deployment Logs")
    print("=" * 50)
    get_deploy_logs()