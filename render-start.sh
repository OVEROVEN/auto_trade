#!/bin/bash

# Render startup script for AI Trading System
echo "🚀 Starting AI Trading System on Render..."

# Create logs directory if it doesn't exist
mkdir -p logs

# Set default environment variables if not provided
export ENVIRONMENT=${ENVIRONMENT:-production}
export DEBUG=${DEBUG:-false}
export PORT=${PORT:-8000}
export OPENAI_API_KEY=${OPENAI_API_KEY:-dummy_key_for_demo}
export DATABASE_URL=${DATABASE_URL:-sqlite:///./trading.db}
export DATABASE_PASSWORD=${DATABASE_PASSWORD:-render_password}
export API_HOST=${API_HOST:-0.0.0.0}

# JWT Configuration
export JWT_SECRET_KEY=${JWT_SECRET_KEY:-$(python -c "import secrets; print(secrets.token_urlsafe(32))")}
export JWT_ALGORITHM=${JWT_ALGORITHM:-HS256}
export JWT_EXPIRE_HOURS=${JWT_EXPIRE_HOURS:-24}

# Google OAuth (will need to be set in Render dashboard)
export GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID:-}
export GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET:-}

# Email settings (optional)
export SMTP_SERVER=${SMTP_SERVER:-smtp.gmail.com}
export SMTP_PORT=${SMTP_PORT:-587}

echo "✅ Environment configured"
echo "   - Environment: $ENVIRONMENT"
echo "   - Port: $PORT"
echo "   - Debug: $DEBUG"

# Start the application
echo "🔥 Starting FastAPI server..."
exec python -m uvicorn src.api.main:app --host 0.0.0.0 --port $PORT --workers 2