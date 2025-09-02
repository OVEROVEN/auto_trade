FROM python:3.11-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴文件
COPY requirements-core.txt .

# 安裝Python依賴
RUN pip install --no-cache-dir -r requirements-core.txt

# 複製應用代碼
COPY src/ ./src/
COPY config/ ./config/

# 設置環境變數
ENV PYTHONPATH=/app
ENV ENVIRONMENT=production
ENV DEBUG=false
ENV DATABASE_URL=sqlite:///tmp/trading.db

# Cloud Run會自動設置$PORT環境變數
ENV PORT=8080
EXPOSE $PORT

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# 啟動命令
CMD python -m uvicorn src.api.main:app --host 0.0.0.0 --port $PORT --workers 1