#!/usr/bin/env python3
"""
檢查最新部署狀態
"""
import requests
import json

def check_deploy_status():
    api_key = "rnd_NB5KFN6sdsZxaC1gaaH2wcbAYRWS"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    service_id = "srv-d2q76dje5dus73bo3hb0"
    deploy_id = "dep-d2qjfqmr433s73edd160"
    
    print("📊 Checking deployment status...")
    print(f"🆔 Deploy ID: {deploy_id}")
    
    try:
        # 檢查部署狀態
        deploy_response = requests.get(
            f"https://api.render.com/v1/services/{service_id}/deploys/{deploy_id}",
            headers=headers
        )
        
        if deploy_response.status_code == 200:
            deploy_data = deploy_response.json()
            status = deploy_data.get("status")
            created_at = deploy_data.get("createdAt")
            finished_at = deploy_data.get("finishedAt")
            
            print(f"📊 Status: {status}")
            print(f"⏰ Created: {created_at}")
            print(f"🏁 Finished: {finished_at}")
            
            if status == "build_failed" or status == "deploy_failed":
                print("❌ Deployment failed!")
                
                # 嘗試獲取錯誤日誌
                logs_response = requests.get(
                    f"https://api.render.com/v1/services/{service_id}/deploys/{deploy_id}/logs",
                    headers=headers
                )
                
                if logs_response.status_code == 200:
                    logs = logs_response.json()
                    print("\n📝 Error Logs:")
                    print("-" * 50)
                    for log in logs[-10:]:
                        print(f"[{log.get('timestamp', '')}] {log.get('message', '')}")
                        
            elif status == "live":
                print("✅ Deployment successful!")
            else:
                print(f"⏳ Still in progress: {status}")
                
        else:
            print(f"❌ Failed to get deploy status: {deploy_response.status_code}")
            print(f"Response: {deploy_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    check_deploy_status()