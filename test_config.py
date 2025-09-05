#!/usr/bin/env python3
"""
🔧 配置測試工具

用於驗證環境變數配置是否正確設定
使用方法: python test_config.py
"""

import os
import sys
from dotenv import load_dotenv

def main():
    print("🔧 AI Trading System - 配置檢查工具")
    print("=" * 50)
    
    # 載入 .env 檔案
    load_dotenv()
    
    try:
        from config import validate_configuration, get_service_status
        
        print("✅ 統一配置模塊已載入")
        print("\n📊 服務狀態:")
        
        status = get_service_status()
        for service, info in status.items():
            print(f"\n🔹 {service.title()}:")
            if isinstance(info, dict):
                for key, value in info.items():
                    if "configured" in key:
                        status_icon = "✅" if value else "❌"
                        print(f"  {status_icon} {key}: {value}")
                    else:
                        print(f"  📋 {key}: {value}")
        
        print("\n🔍 配置驗證:")
        validation = validate_configuration()
        
        if validation['valid']:
            print("✅ 所有關鍵配置都正確")
        else:
            print("❌ 發現配置問題")
        
        if validation['issues']:
            print("\n🚨 嚴重問題:")
            for issue in validation['issues']:
                print(f"  ❌ {issue}")
        
        if validation['warnings']:
            print("\n⚠️  警告:")
            for warning in validation['warnings']:
                print(f"  ⚠️  {warning}")
                
    except ImportError:
        print("❌ 統一配置模塊不可用，使用基礎檢查")
        print("\n📋 環境變數檢查:")
        
        # 基礎環境變數檢查
        env_vars = {
            'OPENAI_API_KEY': '🤖 OpenAI API',
            'GOOGLE_CLIENT_ID': '🔐 Google OAuth Client ID',
            'GOOGLE_CLIENT_SECRET': '🔐 Google OAuth Secret',
            'JWT_SECRET': '🔑 JWT Secret',
            'DATABASE_URL': '🗄️ Database URL'
        }
        
        for var, desc in env_vars.items():
            value = os.getenv(var)
            if value:
                if 'secret' in var.lower() or 'key' in var.lower():
                    display_value = f"{value[:8]}..." if len(value) > 8 else "***"
                else:
                    display_value = value[:50] + "..." if len(value) > 50 else value
                print(f"  ✅ {desc}: {display_value}")
            else:
                print(f"  ❌ {desc}: 未設定")
    
    print("\n" + "=" * 50)
    print("🎯 設定建議:")
    print("1. 複製 .env.example 為 .env")
    print("2. 填入您的實際 API keys")
    print("3. 重新執行此檢查工具")
    print("4. 檢查 SECURITY_CLEANUP_GUIDE.md 以確保安全")

if __name__ == "__main__":
    main()