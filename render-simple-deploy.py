#!/usr/bin/env python3
"""
簡化版Render部署 - 獲取用戶信息並部署
"""
import requests
import json

def get_user_info():
    """獲取Render用戶信息"""
    api_key = "rnd_5xenFgugKDUpkPUHExSwyIYnYYZY"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    print("👤 Getting user information...")
    
    try:
        response = requests.get("https://api.render.com/v1/users", headers=headers)
        if response.status_code == 200:
            users = response.json()
            if users:
                user_id = users[0].get("id")
                email = users[0].get("email")
                print(f"✅ User ID: {user_id}")
                print(f"📧 Email: {email}")
                return user_id
        else:
            print(f"❌ Error getting user info: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def deploy_with_owner_id(owner_id):
    """使用Owner ID部署到Render"""
    api_key = "rnd_5xenFgugKDUpkPUHExSwyIYnYYZY"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    service_config = {
        "type": "web_service",
        "name": "auto-trade-core",
        "ownerId": owner_id,
        "repo": "https://github.com/OVEROVEN/auto_trade",
        "branch": "master",
        "runtime": "python",
        "buildCommand": "pip install -r requirements-core.txt",
        "startCommand": "python -m uvicorn src.api.main_core:app --host 0.0.0.0 --port $PORT",
        "plan": "free",
        "region": "oregon",
        "envVars": [
            {"key": "ENVIRONMENT", "value": "production"},
            {"key": "DEBUG", "value": "false"},
            {"key": "SERVICE_NAME", "value": "core-api"},
            {"key": "DATABASE_URL", "value": "sqlite:///./data/trading.db"}
        ]
    }
    
    print("🚀 Creating Render service with Owner ID...")
    
    try:
        response = requests.post(
            "https://api.render.com/v1/services",
            headers=headers,
            json=service_config
        )
        
        if response.status_code == 201:
            service_data = response.json()
            service_id = service_data.get("id")
            service_url = service_data.get("serviceDetails", {}).get("url", "")
            
            print(f"✅ Service created successfully!")
            print(f"🆔 Service ID: {service_id}")
            print(f"🌐 Service URL: {service_url}")
            print(f"📄 API Docs: {service_url}/docs")
            print(f"💓 Health: {service_url}/health")
            
            return service_id, service_url
        else:
            print(f"❌ Failed to create service: {response.status_code}")
            print(f"Response: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None, None

if __name__ == "__main__":
    print("🎯 Render Deployment - Simple Version")
    print("=" * 40)
    
    # 獲取用戶ID
    owner_id = get_user_info()
    
    if owner_id:
        # 部署服務
        service_id, service_url = deploy_with_owner_id(owner_id)
        
        if service_id:
            print("\n🎉 Deployment initiated successfully!")
            print("⏰ Please wait 5-10 minutes for build to complete")
            print("📊 Check Render dashboard for build progress")
        else:
            print("\n❌ Deployment failed")
    else:
        print("\n❌ Failed to get user information")
        print("🔧 Manual deployment required")