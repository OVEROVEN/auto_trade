#!/usr/bin/env python3
"""
使用Render API自動部署
"""
import requests
import json
import time

def deploy_to_render():
    """使用Render API部署服務"""
    
    # Render API配置
    api_key = "rnd_5xenFgugKDUpkPUHExSwyIYnYYZY"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 服務配置
    service_config = {
        "type": "web_service",
        "name": "auto-trade-core",
        "ownerId": None,  # 將自動使用您的用戶ID
        "repo": "https://github.com/OVEROVEN/auto_trade.git",
        "branch": "master",
        "rootDir": ".",
        "runtime": "python",
        "buildCommand": "pip install -r requirements-core.txt",
        "startCommand": "python -m uvicorn src.api.main:app --host 0.0.0.0 --port $PORT",
        "plan": "free",
        "region": "oregon",
        "envVars": [
            {"key": "ENVIRONMENT", "value": "production"},
            {"key": "DEBUG", "value": "false"},
            {"key": "SERVICE_NAME", "value": "core-api"},
            {"key": "DATABASE_URL", "value": "sqlite:///tmp/trading.db"},
            {"key": "JWT_SECRET_KEY", "value": "pI3tqLLwskk4HQ4fSlLOo32VuRsllB3Z_1eMzgrqjmY"},
            {"key": "GOOGLE_CLIENT_ID", "value": "610357573971-t2r6c0b3i8fq8kng1j8e5s4l6jiqiggf.apps.googleusercontent.com"}
        ]
    }
    
    print("🚀 Starting Render deployment...")
    
    try:
        # 創建服務
        print("📦 Creating Render service...")
        response = requests.post(
            "https://api.render.com/v1/services",
            headers=headers,
            json=service_config
        )
        
        if response.status_code == 201:
            service_data = response.json()
            service_id = service_data.get("id")
            service_url = service_data.get("serviceDetails", {}).get("url")
            
            print(f"✅ Service created successfully!")
            print(f"📋 Service ID: {service_id}")
            print(f"🌐 Service URL: {service_url}")
            
            # 監控部署狀態
            print("⏳ Monitoring deployment...")
            for i in range(30):  # 最多等待15分鐘
                deploy_response = requests.get(
                    f"https://api.render.com/v1/services/{service_id}",
                    headers=headers
                )
                
                if deploy_response.status_code == 200:
                    deploy_data = deploy_response.json()
                    status = deploy_data.get("serviceDetails", {}).get("status")
                    print(f"📊 Status: {status}")
                    
                    if status == "live":
                        print("🎉 Deployment successful!")
                        print(f"🌐 Your app is live at: {service_url}")
                        print(f"📄 API docs: {service_url}/docs")
                        print(f"💓 Health check: {service_url}/health")
                        return True
                    elif status in ["deploy_failed", "failed"]:
                        print("❌ Deployment failed!")
                        return False
                
                time.sleep(30)  # 等待30秒
            
            print("⏰ Deployment monitoring timeout")
            return False
            
        else:
            print(f"❌ Failed to create service: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Deployment error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 Auto-Trade System - Render Deployment")
    print("=" * 50)
    
    success = deploy_to_render()
    
    if success:
        print("\n🎉 Deployment completed successfully!")
        print("📋 Next steps:")
        print("1. Test your deployed API")
        print("2. Set up environment variables if needed")
        print("3. Configure custom domain (optional)")
    else:
        print("\n❌ Deployment failed")
        print("📋 Troubleshooting:")
        print("1. Check Render dashboard for errors")
        print("2. Verify GitHub repository access")
        print("3. Check API key permissions")