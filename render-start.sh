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

echo "✅ Environment configured"
echo "   - Environment: $ENVIRONMENT"
echo "   - Port: $PORT"
echo "   - Debug: $DEBUG"

# Start the application
echo "🔥 Starting FastAPI server..."
exec python -m uvicorn src.api.main:app --host 0.0.0.0 --port $PORT --workers 2