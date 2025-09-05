#!/usr/bin/env python3
"""
觸發新的Render部署
"""
import requests
import json

def trigger_deploy():
    api_key = "rnd_NB5KFN6sdsZxaC1gaaH2wcbAYRWS"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    service_id = "srv-d2q76dje5dus73bo3hb0"  # auto-trade-core
    
    print("🚀 Triggering new deployment for auto-trade-core...")
    
    try:
        # 觸發手動部署
        deploy_response = requests.post(
            f"https://api.render.com/v1/services/{service_id}/deploys",
            headers=headers
        )
        
        if deploy_response.status_code == 201:
            deploy_data = deploy_response.json()
            deploy_id = deploy_data.get("id")
            print(f"✅ Deployment triggered successfully!")
            print(f"🆔 Deploy ID: {deploy_id}")
            print(f"📊 Status: {deploy_data.get('status')}")
            print(f"🌐 Monitor at: https://dashboard.render.com/web/{service_id}")
            return True
        else:
            print(f"❌ Failed to trigger deployment: {deploy_response.status_code}")
            print(f"Response: {deploy_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 Render Deployment Trigger")
    print("=" * 40)
    
    success = trigger_deploy()
    
    if success:
        print("\n🎉 Deployment initiated!")
        print("⏰ Please wait 3-5 minutes for deployment to complete")
        print("🔍 Check Render dashboard for progress")
        print("💓 Test health endpoint: https://auto-trade-core.onrender.com/health")
    else:
        print("\n❌ Failed to trigger deployment")