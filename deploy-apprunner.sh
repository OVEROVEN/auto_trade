#!/bin/bash
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
aws cloudformation create-stack \
    --stack-name auto-trade-apprunner \
    --template-body file://apprunner-cloudformation.yaml \
    --parameters \
        ParameterKey=RepositoryUrl,ParameterValue=https://github.com/OVEROVEN/auto_trade \
        ParameterKey=Branch,ParameterValue=master \
        ParameterKey=OpenAIApiKey,ParameterValue="${OPENAI_API_KEY:-dummy_key}" \
        ParameterKey=GoogleClientSecret,ParameterValue="${GOOGLE_CLIENT_SECRET:-dummy_secret}" \
    --capabilities CAPABILITY_IAM

echo "⏳ Waiting for stack creation to complete..."
aws cloudformation wait stack-create-complete --stack-name auto-trade-apprunner

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    
    # 獲取服務URL
    SERVICE_URL=$(aws cloudformation describe-stacks \
        --stack-name auto-trade-apprunner \
        --query 'Stacks[0].Outputs[?OutputKey==`ServiceUrl`].OutputValue' \
        --output text)
    
    echo "🌐 Service URL: $SERVICE_URL"
    echo "💓 Health check: $SERVICE_URL/health"
    echo "📄 API docs: $SERVICE_URL/docs"
else
    echo "❌ Deployment failed!"
    exit 1
fi
