# 簡化版本 - 只部署後端API
FROM python:3.11-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 使用最小化依賴
COPY requirements-minimal.txt .
RUN pip install --no-cache-dir -r requirements-minimal.txt

# 複製後端代碼
COPY src/ ./src/
COPY config/ ./config/

# 設置環境變數
ENV PYTHONPATH=/app
ENV ENVIRONMENT=production
ENV DEBUG=false
ENV DATABASE_URL=sqlite:///tmp/trading.db

# Cloud Run端口設置
ENV PORT=8080
EXPOSE $PORT

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# 啟動API服務
CMD ["python", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]