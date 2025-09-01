#!/usr/bin/env python3
"""
部署前檢查腳本
確保所有兌換碼功能和核心API正常運作
"""

import asyncio
import sys
import os
import json
import traceback
from datetime import datetime

# 設定路徑
sys.path.append(os.path.dirname(__file__))

async def check_imports():
    """檢查關鍵模組導入"""
    print("🔍 檢查模組導入...")
    
    try:
        # 核心API模組
        from src.api.main import app
        print("✅ 主API模組導入成功")
        
        # 兌換碼相關模組
        from src.api.redemption_endpoints import router as redemption_router
        from src.database.redemption_models import RedemptionCode, RedemptionHistory
        print("✅ 兌換碼模組導入成功")
        
        # 認證模組
        from src.auth.auth import get_current_user
        from src.auth.models import User, FreeQuota
        print("✅ 認證模組導入成功")
        
        # 數據分析模組
        from src.data_fetcher.us_stocks import USStockDataFetcher
        from src.analysis.technical_indicators import IndicatorAnalyzer
        print("✅ 數據分析模組導入成功")
        
        return True
    except Exception as e:
        print(f"❌ 模組導入失敗: {e}")
        traceback.print_exc()
        return False

async def check_database():
    """檢查數據庫連接"""
    print("\n📁 檢查數據庫...")
    
    try:
        from src.database.connection import get_db
        from src.database.redemption_models import RedemptionCode
        
        with get_db() as db:
            # 檢查兌換碼表
            codes = db.query(RedemptionCode).filter(
                RedemptionCode.is_active == True,
                RedemptionCode.is_used == False
            ).limit(5).all()
            
            print(f"✅ 數據庫連接正常，找到 {len(codes)} 個可用兌換碼")
            
            # 列出可用兌換碼
            for code in codes:
                print(f"   🎫 {code.code} - {code.credits} 次")
            
        return True
    except Exception as e:
        print(f"❌ 數據庫檢查失敗: {e}")
        traceback.print_exc()
        return False

async def check_api_endpoints():
    """檢查關鍵API端點"""
    print("\n🌐 檢查API端點...")
    
    try:
        from src.api.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # 檢查健康狀態
        response = client.get("/health")
        if response.status_code == 200:
            print("✅ 健康檢查端點正常")
        else:
            print(f"⚠️ 健康檢查狀態碼: {response.status_code}")
        
        # 檢查股票代碼端點
        response = client.get("/symbols")
        if response.status_code == 200:
            symbols_data = response.json()
            print(f"✅ 股票代碼端點正常 (US: {len(symbols_data.get('us_symbols', []))}, TW: {len(symbols_data.get('tw_symbols', []))})")
        else:
            print(f"⚠️ 股票代碼端點狀態碼: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ API端點檢查失敗: {e}")
        traceback.print_exc()
        return False

async def check_environment_vars():
    """檢查環境變數"""
    print("\n🔧 檢查環境變數...")
    
    required_vars = [
        'OPENAI_API_KEY',
        'JWT_SECRET_KEY', 
        'GOOGLE_CLIENT_ID',
        'GOOGLE_CLIENT_SECRET'
    ]
    
    optional_vars = [
        'DATABASE_URL',
        'ENVIRONMENT',
        'DEBUG'
    ]
    
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value and len(value) > 10:  # 基本長度檢查
            print(f"✅ {var}: 已設置")
        else:
            print(f"❌ {var}: 未設置或太短")
            all_good = False
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"⚠️ {var}: 未設置")
    
    return all_good

async def check_redemption_functionality():
    """檢查兌換碼功能"""
    print("\n🎫 檢查兌換碼功能...")
    
    try:
        from src.database.connection import get_db
        from src.database.redemption_models import RedemptionCode
        from datetime import datetime, timedelta
        
        with get_db() as db:
            # 檢查是否有測試兌換碼
            test_codes = [
                'WEILIANG100X',  # 12字符
                'SOCCER100FANS',  # 13字符
                'NEWUSER20TEST',  # 13字符
            ]
            
            available_codes = []
            for code_str in test_codes:
                code = db.query(RedemptionCode).filter(
                    RedemptionCode.code == code_str,
                    RedemptionCode.is_active == True
                ).first()
                
                if code:
                    if not code.is_used:
                        available_codes.append(code_str)
                        print(f"✅ 測試兌換碼 {code_str} 可用 ({len(code_str)} 字符)")
                    else:
                        print(f"⚠️ 測試兌換碼 {code_str} 已使用")
                else:
                    print(f"❌ 測試兌換碼 {code_str} 不存在")
            
            if available_codes:
                print(f"✅ 兌換碼功能準備就緒，{len(available_codes)} 個測試碼可用")
                return True
            else:
                print("⚠️ 沒有可用的測試兌換碼")
                return False
            
    except Exception as e:
        print(f"❌ 兌換碼功能檢查失敗: {e}")
        traceback.print_exc()
        return False

async def create_deployment_summary():
    """創建部署摘要"""
    print("\n📋 生成部署摘要...")
    
    summary = {
        "deployment_timestamp": datetime.now().isoformat(),
        "api_version": "2.0.0",
        "features": [
            "stock_analysis",
            "redemption_codes",
            "ai_recommendations",
            "user_authentication",
            "real_time_websockets",
            "pattern_recognition"
        ],
        "environment": {
            "python_version": sys.version.split()[0],
            "platform": sys.platform
        },
        "deployment_config": {
            "dockerfile": "Dockerfile.core",
            "requirements": "requirements-core.txt",
            "entry_point": "src.api.main:app",
            "port": "PORT (Railway 動態)"
        }
    }
    
    # 保存摘要
    with open('deployment-summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print("✅ 部署摘要已保存到 deployment-summary.json")
    return summary

async def main():
    """主要檢查流程"""
    print("🚀 AI交易系統部署前檢查")
    print("=" * 50)
    
    checks = [
        ("模組導入", check_imports),
        ("數據庫", check_database), 
        ("API端點", check_api_endpoints),
        ("環境變數", check_environment_vars),
        ("兌換碼功能", check_redemption_functionality),
    ]
    
    all_passed = True
    results = {}
    
    for check_name, check_func in checks:
        try:
            result = await check_func()
            results[check_name] = result
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name}檢查出現異常: {e}")
            results[check_name] = False
            all_passed = False
    
    # 創建部署摘要
    await create_deployment_summary()
    
    print("\n" + "=" * 50)
    print("🎯 檢查結果摘要:")
    
    for check_name, result in results.items():
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"   {check_name}: {status}")
    
    if all_passed:
        print("\n🎊 所有檢查通過！系統準備就緒，可以部署到Railway")
        print("\n📝 部署指令:")
        print("   railway up")
        print("   或使用自動化腳本: python railway-deployment.js")
    else:
        print("\n⚠️ 部分檢查失敗，請修復後再部署")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(main())