#!/bin/bash
# Render startup script for auto-trade-core

echo "🚀 Starting Auto-Trade Core Service on Render..."
echo "📊 Environment: $ENVIRONMENT"
echo "🔧 Debug: $DEBUG"
echo "🌐 Port: $PORT"

# 設置Python路徑
export PYTHONPATH=/opt/render/project/src

# 確保端口設置
export PORT=${PORT:-10000}

echo "🐍 Python path: $PYTHONPATH"
echo "📡 Starting uvicorn on port $PORT..."

# 啟動服務
python -m uvicorn src.api.main_core:app \
    --host 0.0.0.0 \
    --port $PORT \
    --workers 1 \
    --log-level info