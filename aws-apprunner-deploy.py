#!/usr/bin/env python3
"""
AWS App Runner部署配置
最簡單的AWS容器部署方案
"""

# App Runner服務配置
apprunner_yaml = '''
version: 1.0
runtime: python3
build:
  commands:
    build:
      - echo "Installing dependencies..."
      - pip install -r requirements-simple.txt
run:
  runtime-version: 3.11
  command: python -m uvicorn src.api.main_core:app --host 0.0.0.0 --port 8000
  network:
    port: 8000
  env:
    - name: ENVIRONMENT
      value: production
    - name: DEBUG
      value: false
    - name: SERVICE_NAME
      value: auto-trade-core
    - name: DATABASE_URL
      value: sqlite:///./data/trading.db
'''

# CloudFormation template for App Runner
cloudformation_template = '''
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Auto-Trade Core API on AWS App Runner'

Parameters:
  RepositoryUrl:
    Type: String
    Description: GitHub repository URL
    Default: "https://github.com/OVEROVEN/auto_trade"
  
  Branch:
    Type: String
    Description: GitHub branch
    Default: "master"
    
  OpenAIApiKey:
    Type: String
    Description: OpenAI API Key
    NoEcho: true
    Default: ""
    
  GoogleClientSecret:
    Type: String
    Description: Google OAuth Client Secret  
    NoEcho: true
    Default: ""

Resources:
  AutoTradeAppRunnerService:
    Type: AWS::AppRunner::Service
    Properties:
      ServiceName: auto-trade-core
      SourceConfiguration:
        AutoDeploymentsEnabled: true
        CodeRepository:
          RepositoryUrl: !Ref RepositoryUrl
          SourceCodeVersion:
            Type: BRANCH
            Value: !Ref Branch
          CodeConfiguration:
            ConfigurationSource: CONFIGURATION_FILE
            CodeConfigurationValues:
              Runtime: PYTHON_3
              BuildCommand: pip install -r requirements-simple.txt
              StartCommand: python -m uvicorn src.api.main_core:app --host 0.0.0.0 --port 8000
              Port: 8000
              RuntimeEnvironmentVariables:
                - Name: ENVIRONMENT
                  Value: production
                - Name: DEBUG
                  Value: false
                - Name: SERVICE_NAME
                  Value: auto-trade-core
                - Name: DATABASE_URL
                  Value: "sqlite:///./data/trading.db"
                - Name: OPENAI_API_KEY
                  Value: !Ref OpenAIApiKey
                - Name: GOOGLE_CLIENT_SECRET
                  Value: !Ref GoogleClientSecret
      InstanceConfiguration:
        Cpu: 0.25 vCPU
        Memory: 0.5 GB

Outputs:
  ServiceUrl:
    Description: App Runner service URL
    Value: !GetAtt AutoTradeAppRunnerService.ServiceUrl
  ServiceArn:
    Description: App Runner service ARN
    Value: !GetAtt AutoTradeAppRunnerService.ServiceArn
'''

import os

def create_apprunner_config():
    """創建AWS App Runner配置"""
    
    print("🚀 Creating AWS App Runner deployment configuration...")
    
    # 創建apprunner.yaml
    with open('apprunner.yaml', 'w') as f:
        f.write(apprunner_yaml)
    print("✅ Created apprunner.yaml")
    
    # 創建CloudFormation template
    with open('apprunner-cloudformation.yaml', 'w') as f:
        f.write(cloudformation_template)
    print("✅ Created apprunner-cloudformation.yaml")
    
    # 創建部署腳本
    deploy_script = '''#!/bin/bash
# AWS App Runner 部署腳本

echo "🚀 Deploying Auto-Trade Core to AWS App Runner..."

# 檢查AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Install with: pip install awscli"
    exit 1
fi

# 檢查AWS配置
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS not configured. Run: aws configure"
    exit 1
fi

echo "📦 Creating CloudFormation stack..."

# 部署CloudFormation stack
aws cloudformation create-stack \\
    --stack-name auto-trade-apprunner \\
    --template-body file://apprunner-cloudformation.yaml \\
    --parameters \\
        ParameterKey=RepositoryUrl,ParameterValue=https://github.com/OVEROVEN/auto_trade \\
        ParameterKey=Branch,ParameterValue=master \\
        ParameterKey=OpenAIApiKey,ParameterValue="${OPENAI_API_KEY:-dummy_key}" \\
        ParameterKey=GoogleClientSecret,ParameterValue="${GOOGLE_CLIENT_SECRET:-dummy_secret}" \\
    --capabilities CAPABILITY_IAM

echo "⏳ Waiting for stack creation to complete..."
aws cloudformation wait stack-create-complete --stack-name auto-trade-apprunner

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    
    # 獲取服務URL
    SERVICE_URL=$(aws cloudformation describe-stacks \\
        --stack-name auto-trade-apprunner \\
        --query 'Stacks[0].Outputs[?OutputKey==`ServiceUrl`].OutputValue' \\
        --output text)
    
    echo "🌐 Service URL: $SERVICE_URL"
    echo "💓 Health check: $SERVICE_URL/health"
    echo "📄 API docs: $SERVICE_URL/docs"
else
    echo "❌ Deployment failed!"
    exit 1
fi
'''
    
    with open('deploy-apprunner.sh', 'w') as f:
        f.write(deploy_script)
    os.chmod('deploy-apprunner.sh', 0o755)
    print("✅ Created deploy-apprunner.sh")
    
    print("\n🎯 AWS App Runner deployment ready!")
    print("📋 Deployment options:")
    print("  Option 1 - Script: ./deploy-apprunner.sh")
    print("  Option 2 - Manual: Upload apprunner-cloudformation.yaml to AWS Console")
    print("  Option 3 - CLI: aws cloudformation create-stack...")

if __name__ == "__main__":
    create_apprunner_config()