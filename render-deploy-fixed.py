#!/usr/bin/env python3
"""
修復版Render API部署腳本
"""
import requests
import json
import time

def get_user_info(api_key):
    """獲取用戶信息"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get("https://api.render.com/v1/owners", headers=headers)
        if response.status_code == 200:
            owners = response.json()
            if owners:
                return owners[0]["owner"]["id"]
        return None
    except Exception as e:
        print(f"獲取用戶信息失敗: {e}")
        return None

def deploy_to_render():
    """使用Render API部署服務"""
    
    # Render API配置
    api_key = "rnd_5xenFgugKDUpkPUHExSwyIYnYYZY"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("🔍 Getting user information...")
    owner_id = get_user_info(api_key)
    
    if not owner_id:
        print("❌ Failed to get user ID")
        return False
    
    print(f"✅ Owner ID: {owner_id}")
    
    # 服務配置
    service_config = {
        "type": "web_service",
        "name": "auto-trade-core-v2",
        "ownerId": owner_id,
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
            {"key": "DATABASE_URL", "value": "sqlite:///tmp/trading.db"},
            {"key": "JWT_SECRET_KEY", "value": "pI3tqLLwskk4HQ4fSlLOo32VuRsllB3Z_1eMzgrqjmY"},
            {"key": "GOOGLE_CLIENT_ID", "value": "610357573971-t2r6c0b3i8fq8kng1j8e5s4l6jiqiggf.apps.googleusercontent.com"},
            {"key": "OPENAI_API_KEY", "value": "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"}
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
        
        print(f"Response status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            service_data = response.json()
            service_id = service_data.get("id")
            service_url = service_data.get("serviceDetails", {}).get("url")
            
            print(f"✅ Service created successfully!")
            print(f"📋 Service ID: {service_id}")
            print(f"🌐 Service URL: {service_url}")
            
            # 監控部署狀態
            print("⏳ Monitoring deployment...")
            for i in range(20):  # 最多等待10分鐘
                try:
                    deploy_response = requests.get(
                        f"https://api.render.com/v1/services/{service_id}",
                        headers=headers
                    )
                    
                    if deploy_response.status_code == 200:
                        deploy_data = deploy_response.json()
                        status = deploy_data.get("status", "unknown")
                        print(f"📊 Status: {status}")
                        
                        if status == "live":
                            print("🎉 Deployment successful!")
                            print(f"🌐 Your app is live at: {service_url}")
                            print(f"📄 API docs: {service_url}/docs")
                            print(f"💓 Health check: {service_url}/health")
                            
                            # 測試服務
                            print("\n🧪 Testing deployed service...")
                            try:
                                test_response = requests.get(f"{service_url}/health", timeout=10)
                                if test_response.status_code == 200:
                                    print("✅ Service is responding!")
                                    print(f"Response: {test_response.json()}")
                                else:
                                    print(f"⚠️ Service returned: {test_response.status_code}")
                            except Exception as e:
                                print(f"⚠️ Service test failed: {e}")
                            
                            return True, service_url
                        elif status in ["deploy_failed", "failed"]:
                            print("❌ Deployment failed!")
                            return False, None
                        elif status in ["building", "deploying"]:
                            print(f"⏳ Still {status}...")
                    
                    time.sleep(30)  # 等待30秒
                except Exception as e:
                    print(f"⚠️ Status check error: {e}")
                    time.sleep(30)
            
            print("⏰ Deployment monitoring timeout")
            return False, None
            
        else:
            print(f"❌ Failed to create service: {response.status_code}")
            print(f"Error: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Deployment error: {str(e)}")
        return False, None

if __name__ == "__main__":
    print("🎯 AI交易系統 - Render部署 (修復版)")
    print("=" * 50)
    
    success, url = deploy_to_render()
    
    if success:
        print(f"\n🎉 部署完全成功！")
        print(f"🌐 服務URL: {url}")
        print(f"📚 API文檔: {url}/docs") 
        print(f"💚 健康檢查: {url}/health")
        print(f"🎫 兌換碼API: {url}/api/redemption/credits")
        print("\n🎯 下一步:")
        print("1. 測試兌換碼功能")
        print("2. 驗證所有API端點") 
        print("3. 開始使用您的AI交易系統！")
    else:
        print(f"\n❌ Render部署失敗")
        print("\n💡 大廠替代方案建議:")
        print("1. 🚀 AWS App Runner - 最穩定")
        print("2. ☁️ Google Cloud Run - 免費額度充足") 
        print("3. 🔵 Azure Container Apps - 企業級")
        print("\n我可以立即幫您設置以上任一平台！")