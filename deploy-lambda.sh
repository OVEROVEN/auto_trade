#!/bin/bash
# AWS Lambda 部署腳本

echo "🚀 Deploying Auto-Trade Core to AWS Lambda..."

# 安裝依賴
pip install -r requirements-lambda.txt -t .

# 使用SAM部署
sam build
sam deploy --guided

echo "✅ Deployment complete!"
echo "📊 Check AWS Console for API Gateway URL"
