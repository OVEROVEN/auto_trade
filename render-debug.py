#!/usr/bin/env python3
"""
Debug Render API response
"""
import requests
import json

def debug_render():
    api_key = "rnd_NB5KFN6sdsZxaC1gaaH2wcbAYRWS"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    print("🔍 Debug Render API...")
    
    try:
        # 獲取服務列表
        response = requests.get("https://api.render.com/v1/services", headers=headers)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Raw Response:")
        print(json.dumps(response.json(), indent=2))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_render()