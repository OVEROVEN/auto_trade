#!/usr/bin/env python3
"""
快速部署到Render平台
更穩定的替代方案
"""
import os
import subprocess
import json

def setup_render_deployment():
    """設置Render部署"""
    
    print("🚀 Setting up Render deployment...")
    
    # 創建render.yaml配置文件
    render_config = {
        "services": [
            {
                "type": "web",
                "name": "auto-trade-core",
                "env": "python",
                "buildCommand": "pip install -r requirements-core.txt",
                "startCommand": "python -m uvicorn src.api.main_core:app --host 0.0.0.0 --port $PORT",
                "envVars": [
                    {"key": "ENVIRONMENT", "value": "production"},
                    {"key": "DEBUG", "value": "false"},
                    {"key": "DATABASE_URL", "value": "sqlite:///./data/trading.db"}
                ]
            }
        ]
    }
    
    with open("render.yaml", "w") as f:
        import yaml
        try:
            yaml.dump(render_config, f)
            print("✅ render.yaml created")
        except ImportError:
            # 如果沒有yaml，用json格式
            with open("render.json", "w") as jf:
                json.dump(render_config, jf, indent=2)
            print("✅ render.json created (YAML not available)")
    
    print("\n📋 Next steps for Render deployment:")
    print("1. Go to https://render.com")
    print("2. Connect your GitHub repository")
    print("3. Choose 'Web Service'")
    print("4. Select this repository")
    print("5. Use these settings:")
    print("   - Build Command: pip install -r requirements-core.txt")
    print("   - Start Command: python -m uvicorn src.api.main_core:app --host 0.0.0.0 --port $PORT")
    print("   - Python Version: 3.11")
    
    print("\n🌐 Alternative: Use Vercel")
    print("1. Go to https://vercel.com")
    print("2. Import GitHub repository")
    print("3. Deploy as Python app")
    
    return True

if __name__ == "__main__":
    setup_render_deployment()