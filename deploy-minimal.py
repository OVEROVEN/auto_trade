#!/usr/bin/env python3
"""
最簡化Railway部署腳本
創建包含最少文件的部署包
"""

import os
import shutil
import subprocess

def create_minimal_deployment():
    """創建最小化部署目錄"""
    deploy_dir = "deploy-minimal"
    
    # 清理舊的部署目錄
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    
    os.makedirs(deploy_dir)
    
    # 複製必要的核心文件
    essential_files = [
        "src/",
        "requirements-core.txt",
        "Dockerfile.core",
        "railway.toml",
        ".railwayignore"
    ]
    
    for item in essential_files:
        src_path = item
        dst_path = os.path.join(deploy_dir, item)
        
        if os.path.isdir(src_path):
            # 複製目錄但排除測試和演示文件
            shutil.copytree(src_path, dst_path, ignore=shutil.ignore_patterns(
                'test_*.py', '*_test.py', '__pycache__', '*.pyc', 'demo_*.py'
            ))
        elif os.path.isfile(src_path):
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
    
    print(f"✅ 創建最小化部署目錄: {deploy_dir}")
    
    # 顯示部署目錄大小
    total_size = 0
    file_count = 0
    for root, dirs, files in os.walk(deploy_dir):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
            file_count += 1
    
    print(f"📊 部署包統計:")
    print(f"   - 文件數量: {file_count}")
    print(f"   - 總大小: {total_size / 1024:.1f} KB")
    
    return deploy_dir

def deploy_to_railway(deploy_dir):
    """從最小化目錄部署到Railway"""
    os.chdir(deploy_dir)
    
    # 初始化git (如果需要)
    if not os.path.exists('.git'):
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Minimal deployment package'], check=True)
    
    # 部署到Railway
    print("🚀 開始Railway部署...")
    result = subprocess.run(['railway', 'up'], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 部署成功！")
        print(result.stdout)
    else:
        print("❌ 部署失敗:")
        print(result.stderr)
    
    return result.returncode == 0

if __name__ == "__main__":
    print("🛠️  創建最小化Railway部署包...")
    
    deploy_dir = create_minimal_deployment()
    
    print(f"\n📋 部署目錄已創建: {deploy_dir}")
    print("💡 你可以手動進入該目錄執行部署:")
    print(f"   cd {deploy_dir}")
    print("   railway up")