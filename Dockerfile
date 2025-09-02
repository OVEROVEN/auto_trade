# Cloud Run 優化版本 - API Only
FROM python:3.11-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 複製並安裝依賴
COPY requirements-minimal.txt .
RUN pip install --no-cache-dir -r requirements-minimal.txt

# 複製應用代碼
COPY src/ ./src/
COPY config/ ./config/

# 創建必要目錄
RUN mkdir -p /tmp/data && chmod 777 /tmp/data

# 設置環境變數
ENV PYTHONPATH=/app
ENV ENVIRONMENT=production
ENV DEBUG=false
ENV DATABASE_URL=sqlite:///tmp/data/trading.db

# Cloud Run會自動注入PORT環境變數
ENV PORT=8080
EXPOSE 8080

# 啟動命令 - 使用環境變數中的PORT
CMD exec python -m uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1 --log-level info