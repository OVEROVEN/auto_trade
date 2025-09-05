#!/usr/bin/env python3
"""
AWS Lambda + API Gateway 部署腳本
最適合FastAPI的AWS解決方案
"""

# 創建Lambda適配器
lambda_handler_content = '''
"""
AWS Lambda handler for FastAPI
"""
try:
    from mangum import Mangum
    from src.api.main_core import app
    
    # 創建Lambda處理器
    handler = Mangum(app, lifespan="off")
    
    # Lambda入口點
    def lambda_handler(event, context):
        return handler(event, context)
        
except ImportError:
    # 如果沒有mangum，創建基本處理器
    def lambda_handler(event, context):
        return {
            'statusCode': 200,
            'body': '{"message": "Auto-Trade Core API - Install mangum for full functionality"}'
        }
'''

# 創建requirements for Lambda
lambda_requirements = '''
# AWS Lambda專用依賴
mangum==0.17.0

# 核心FastAPI
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0

# 數據處理
pandas==2.1.4
numpy==1.25.2
requests==2.31.0
yfinance==0.2.18

# 基礎工具
python-dotenv==1.0.0

# AWS SDK (可選)
boto3==1.34.0
'''

# SAM template for easy deployment
sam_template = '''
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Auto-Trade Core API on AWS Lambda

Globals:
  Function:
    Timeout: 30
    MemorySize: 512
    Environment:
      Variables:
        ENVIRONMENT: production
        DEBUG: false
        SERVICE_NAME: auto-trade-core

Resources:
  AutoTradeCoreFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: ./
      Handler: lambda_handler.lambda_handler
      Runtime: python3.11
      Architectures:
        - x86_64
      Events:
        AutoTradeCore:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
      Environment:
        Variables:
          DATABASE_URL: sqlite:///./data/trading.db
          OPENAI_API_KEY: !Ref OpenAIApiKey
          GOOGLE_CLIENT_ID: "610357573971-t2r6c0b3i8fq8kng1j8e5s4l6jiqiggf.apps.googleusercontent.com"
          GOOGLE_CLIENT_SECRET: !Ref GoogleClientSecret

Parameters:
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

Outputs:
  AutoTradeCoreApi:
    Description: "API Gateway endpoint URL"
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/"
'''

import os

def create_aws_lambda_config():
    """創建AWS Lambda部署配置"""
    
    print("🚀 Creating AWS Lambda deployment configuration...")
    
    # 創建Lambda handler
    with open('lambda_handler.py', 'w') as f:
        f.write(lambda_handler_content)
    print("✅ Created lambda_handler.py")
    
    # 創建Lambda專用requirements
    with open('requirements-lambda.txt', 'w') as f:
        f.write(lambda_requirements)
    print("✅ Created requirements-lambda.txt")
    
    # 創建SAM template
    with open('template.yaml', 'w') as f:
        f.write(sam_template)
    print("✅ Created template.yaml (SAM)")
    
    # 創建部署腳本
    deploy_script = '''#!/bin/bash
# AWS Lambda 部署腳本

echo "🚀 Deploying Auto-Trade Core to AWS Lambda..."

# 安裝依賴
pip install -r requirements-lambda.txt -t .

# 使用SAM部署
sam build
sam deploy --guided

echo "✅ Deployment complete!"
echo "📊 Check AWS Console for API Gateway URL"
'''
    
    with open('deploy-lambda.sh', 'w') as f:
        f.write(deploy_script)
    os.chmod('deploy-lambda.sh', 0o755)
    print("✅ Created deploy-lambda.sh")
    
    print("\n🎯 AWS Lambda deployment ready!")
    print("📋 Next steps:")
    print("1. Install AWS CLI: pip install awscli")
    print("2. Configure AWS: aws configure")
    print("3. Install SAM CLI: pip install aws-sam-cli")
    print("4. Run: ./deploy-lambda.sh")
    print("5. Follow the guided deployment prompts")

if __name__ == "__main__":
    create_aws_lambda_config()