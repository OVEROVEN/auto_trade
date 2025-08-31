#!/usr/bin/env python3
"""
實時監控Railway部署狀態
"""

import requests
import time
from datetime import datetime
import json

def monitor_railway_deployment():
    """監控Railway部署狀態"""
    
    url = "https://autotrade-production-a264.up.railway.app"
    
    print("🔍 開始監控Railway部署狀態...")
    print(f"📡 目標URL: {url}")
    print("=" * 60)
    
    start_time = time.time()
    check_count = 0
    max_checks = 30  # 最多檢查30次 (15分鐘)
    
    while check_count < max_checks:
        check_count += 1
        current_time = datetime.now().strftime("%H:%M:%S")
        elapsed = time.time() - start_time
        
        try:
            print(f"⏱️  [{current_time}] 檢查 #{check_count} (已運行 {elapsed:.1f}s)")
            
            # 檢查根端點
            response = requests.get(f"{url}", timeout=10)
            
            if response.status_code == 200:
                print(f"🎉 根端點響應成功！狀態碼: {response.status_code}")
                try:
                    data = response.json()
                    print(f"📄 響應內容: {json.dumps(data, indent=2)}")
                except:
                    print(f"📄 響應內容 (文本): {response.text[:200]}...")
                break
                
            elif response.status_code == 502:
                print(f"⏳ 服務啟動中... (502 Bad Gateway)")
                
            elif response.status_code == 503:
                print(f"⏳ 服務不可用... (503 Service Unavailable)")
                
            else:
                print(f"⚠️  異常狀態碼: {response.status_code}")
                print(f"📄 響應: {response.text[:100]}...")
                
        except requests.exceptions.ConnectTimeout:
            print(f"⏳ 連接超時，服務可能還在啟動...")
            
        except requests.exceptions.ConnectionError:
            print(f"❌ 連接錯誤，服務可能還沒準備好...")
            
        except Exception as e:
            print(f"❗ 其他錯誤: {str(e)}")
        
        # 如果不是最後一次檢查，等待30秒
        if check_count < max_checks:
            print(f"⏰ 等待30秒後進行下一次檢查...\n")
            time.sleep(30)
    
    # 最終檢查健康端點
    print("\n🏥 檢查健康端點...")
    try:
        health_response = requests.get(f"{url}/health", timeout=10)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ 健康檢查成功: {json.dumps(health_data, indent=2)}")
        else:
            print(f"⚠️  健康檢查狀態碼: {health_response.status_code}")
    except Exception as e:
        print(f"❌ 健康檢查失敗: {str(e)}")
    
    print("\n" + "=" * 60)
    print("📊 監控完成")
    
    if check_count >= max_checks:
        print("⏰ 達到最大檢查次數，請手動檢查Railway Dashboard")
        print("🌐 Railway項目: https://railway.com/project/fe272568-e1ef-45ad-a5d2-a4674491fb8c")
    
    total_time = time.time() - start_time
    print(f"⏱️  總監控時間: {total_time/60:.1f} 分鐘")

if __name__ == "__main__":
    monitor_railway_deployment()