#!/usr/bin/env python3
"""
Railway deployment monitoring - compact version
"""
import requests
import time
from datetime import datetime

def check_railway_service():
    """Quick Railway service check"""
    url = "https://autotrade-production-a264.up.railway.app"
    
    try:
        print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Testing {url}")
        
        # Test health endpoint
        response = requests.get(f"{url}/health", timeout=10)
        print(f"✅ Health: {response.status_code} - {response.text[:100]}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {str(e)}")
        
        try:
            # Try root endpoint
            root_response = requests.get(f"{url}", timeout=5)
            print(f"🔍 Root: {root_response.status_code}")
        except:
            print(f"❌ Root endpoint also failing")
            
        return False

if __name__ == "__main__":
    print("🚀 Railway Service Monitor")
    print("=" * 40)
    
    for i in range(6):  # Check 6 times
        success = check_railway_service()
        if success:
            print("🎉 Service is working!")
            break
        
        if i < 5:
            print("⏱️  Waiting 30 seconds...\n")
            time.sleep(30)
    
    print("📊 Monitoring complete")