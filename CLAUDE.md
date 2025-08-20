# AI Trading System - Claude Assistant Guide

## 📋 Project Overview

This is a comprehensive AI-powered stock trading analysis system built with Python, FastAPI, and integrated AI capabilities.

### 🏗️ System Architecture

```
Frontend (GUI/Web) → FastAPI API → Data Fetchers → Analysis Engine → AI Integration → Response
```

## 🚀 Quick Start Commands

### Start the API Server (With Taiwan Integration)
```bash
# 新版台股整合啟動器 (推薦)
uv run python start_taiwan_system.py

# 或使用傳統方式
uv run python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# 或不使用 uv
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Demo Scripts
```bash
# Taiwan Stock Integration Demo (NEW!)
uv run python start_taiwan_system.py

# Custom TradingView Chart (Latest Feature)
uv run python demo_custom_chart.py

# Interactive Trading Interface
uv run python interactive_trading.py

# Chart Viewer GUI
uv run python chart_viewer.py

# Quick Demo
uv run python quick_demo.py

# System Startup Menu
uv run python start_system.py
```

### Testing Commands
```bash
# Test system setup
python test_setup.py

# Test API components
python test_api_components.py

# Test charts
python test_charts.py

# Test backtesting
python test_backtest.py
```

## 🔧 Development Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Linting/Type Checking
```bash
# Note: No specific lint/typecheck commands found in codebase
# Standard Python tools can be used:
python -m flake8 src/
python -m mypy src/
```

### Docker Commands
```bash
# Start with Docker
docker-compose up -d

# Development environment
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

## 📁 Key File Locations

### Core API
- **Main API**: `src/api/main.py` - FastAPI application with all endpoints
- **Configuration**: `config/settings.py` - System settings and configuration

### Data Layer
- **US Stocks**: `src/data_fetcher/us_stocks.py` - Yahoo Finance integration
- **Taiwan Stocks**: `src/data_fetcher/tw_stocks.py` - Taiwan stock market data

### Analysis Engine
- **Technical Indicators**: `src/analysis/technical_indicators.py` - RSI, MACD, etc.
- **Pattern Recognition**: `src/analysis/pattern_recognition.py` - Chart patterns
- **AI Analysis**: `src/analysis/ai_analyzer.py` - OpenAI integration
- **Advanced Patterns**: `src/analysis/advanced_patterns.py` - Complex chart patterns

### Visualization
- **Chart Generator**: `src/visualization/chart_generator.py` - Basic charts
- **Professional Charts**: `src/visualization/professional_charts.py` - Advanced charts
- **TradingView Integration**: `src/visualization/tradingview_*.py` - TradingView widgets
- **Custom TradingView**: `src/visualization/custom_tradingview.py` - Latest custom implementation

### Strategy & Backtesting
- **Backtest Engine**: `src/backtesting/backtest_engine.py` - Strategy backtesting
- **Pattern Strategy**: `src/strategies/pattern_strategy.py` - Pattern-based trading

## 🌐 API Endpoints Reference

### Core Analysis
- `POST /analyze/{symbol}` - Comprehensive stock analysis
- `GET /signals/{symbol}` - Trading signals
- `GET /patterns/{symbol}` - Pattern detection
- `POST /patterns/advanced/{symbol}` - Advanced pattern analysis

### Charts & Visualization
- `GET /chart/custom/{symbol}` - **Custom TradingView chart (Latest)**
- `GET /chart/tradingview/{symbol}` - TradingView integration
- `GET /chart/professional/{symbol}` - Professional charts
- `GET /chart/performance/{symbol}` - Strategy performance charts

### Taiwan Stock API (NEW! 🇹🇼)
- `GET /api/taiwan/market-overview` - Taiwan market overview
- `GET /api/taiwan/stocks/search` - Search Taiwan stocks
- `GET /api/taiwan/stocks/{symbol}/info` - Stock information
- `GET /api/taiwan/stocks/{symbol}/quote` - Real-time quote
- `POST /api/taiwan/stocks/{symbol}/historical` - Historical data
- `GET /api/taiwan/stocks/popular` - Popular Taiwan stocks

### TradingView Datafeed (NEW! 📊)
- `GET /api/tradingview/config` - Datafeed configuration
- `GET /api/tradingview/symbols` - Symbol search
- `GET /api/tradingview/symbols/{symbol}` - Symbol resolution
- `GET /api/tradingview/history` - Historical bars
- `GET /api/tradingview/time` - Server time

### Market Switching (NEW! 🔄)
- `POST /api/market/switch` - Switch between US/TW markets
- `GET /api/market/info` - Current market information

### Cache Management (NEW! 💾)
- `GET /api/cache/stats` - Cache statistics

### Backtesting
- `POST /backtest` - Run strategy backtest
- `GET /backtest/strategies` - Available strategies

### AI Features
- `POST /ai/discuss-strategy` - AI strategy discussion
- `POST /ai/optimize-backtest` - AI backtest optimization
- `POST /ai/ask` - General AI questions

### System
- `GET /health` - System health check
- `GET /symbols` - Available symbols
- `WS /stream/{symbol}` - Real-time WebSocket

## ⚙️ Configuration Requirements

### Environment Variables (.env file)
```env
# Required for AI features
OPENAI_API_KEY=your_openai_api_key_here

# Optional
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here

# Database (if using)
DATABASE_URL=postgresql://user:pass@localhost:5432/trading_db
DATABASE_PASSWORD=secure_password

# Redis (if using)
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=redis_password
```

## 🎯 Supported Stock Symbols

### US Market
- **Tech**: AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA
- **ETFs**: SPY, QQQ, IWM
- **Others**: NFLX, BABA, AMD

### Taiwan Market
- **Format**: `SYMBOL.TW` (e.g., `2330.TW`)
- **Major stocks**: 2330.TW (TSMC), 2317.TW (Hon Hai)

## 🧪 Testing & Validation

### System Health Check
```bash
curl http://localhost:8000/health
```

### Quick Analysis Test
```bash
curl -X POST "http://localhost:8000/analyze/AAPL" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "period": "3mo", "include_ai": true}'
```

## 🛠️ Available Strategies

1. **pattern_trading** - Pattern-based trading (recommended)
2. **rsi_macd** - RSI + MACD combination
3. **ma_crossover** - Moving average crossover
4. **enhanced_pattern** - Pattern trading with confirmations

## 🚨 Common Issues

### AI Features Not Working
- **Cause**: Missing OpenAI API key
- **Solution**: Set `OPENAI_API_KEY` in `.env` file

### No Data for Symbol
- **Cause**: Invalid symbol format or market hours
- **Solution**: Check symbol format (use `.TW` for Taiwan stocks)

### Connection Errors
- **Cause**: API server not running
- **Solution**: Start with `python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000`

## 📊 Latest Features

### Custom TradingView Chart (NEW)
- **File**: `src/visualization/custom_tradingview.py`
- **Endpoint**: `GET /chart/custom/{symbol}`
- **Demo**: `python demo_custom_chart.py`
- **Features**: K-line + Volume + RSI + AI recommendations + Strategy info

## 🔄 Development Workflow

1. **Start API Server**: `python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000`
2. **Open API Docs**: http://localhost:8000/docs
3. **Test Endpoints**: Use Swagger UI or demo scripts
4. **View Charts**: Access chart endpoints or run demo scripts

## 📝 Code Conventions

- **Python Style**: PEP 8 compliant
- **Async/Await**: Used for API endpoints with AI integration
- **Error Handling**: Comprehensive exception handling with logging
- **Type Hints**: Full type annotations throughout codebase
- **Documentation**: Detailed docstrings for all functions

## 🎪 Demo Scenarios

### Basic Stock Analysis
```python
python demo_simple.py
```

### Professional Charts
```python
python demo_professional_charts.py
```

### Custom TradingView (Your Requirements)
```python
python demo_custom_chart.py
```

### Interactive Trading
```python
python interactive_trading.py
```

## 🌟 System Status

**✅ OPERATIONAL** - All core features working
- Multi-market data support (US + Taiwan)
- Technical analysis engine (15+ indicators)
- AI integration (OpenAI GPT-4)
- Pattern recognition (Classic + Advanced)
- Professional visualization (TradingView)
- Backtesting engine (4 strategies)
- Real-time WebSocket streaming

## 🔄 Git版本控制指南

### 📋 Git最佳實踐
本專案使用Git進行版本控制，以下是推薦的工作流程：

#### 基本Git命令
```bash
# 檢查當前狀態
git status

# 查看提交歷史
git log --oneline -10

# 檢查最近的變更
git diff

# 暫存所有變更
git add -A

# 提交變更（使用描述性訊息）
git commit -m "Fix: 修復技術訊號顯示問題"

# 查看分支
git branch -a
```

#### 提交訊息規範
使用以下格式撰寫提交訊息：
```
類型: 簡短描述

詳細說明（可選）
- 修復的具體問題
- 新增的功能
- 重要的技術細節

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

**提交類型：**
- `Fix:` 修復Bug
- `Add:` 新增功能
- `Update:` 更新現有功能
- `Refactor:` 代碼重構
- `Doc:` 文檔更新
- `Test:` 測試相關

#### 🏷️ 版本標記
```bash
# 創建版本標籤
git tag -a v1.2.0 -m "AI策略分析儀表板完成"

# 查看所有標籤
git tag -l

# 推送標籤到遠程
git push origin v1.2.0
```

#### 📦 當前版本狀態
**最新提交**: `74d28e4` - Fix dashboard technical signals and enhance backtest UI

**主要功能完成度：**
- ✅ 技術訊號分析系統
- ✅ AI策略顧問整合
- ✅ 形態回測引擎
- ✅ 增強版TradingView圖表
- ✅ 多市場數據支援（US + TW）

### 🔧 開發工作流程
1. **功能開發前**: `git status` 檢查乾淨狀態
2. **開發過程中**: 定期檢查 `git diff` 
3. **功能完成後**: `git add -A && git commit -m "描述性訊息"`
4. **重大版本**: 創建標籤標記里程碑

## 🧪 MCP 工具測試與驗證指南

### 🎯 使用MCP工具進行全面測試
善用Claude Code的MCP (Model Context Protocol) 工具套件來測試和驗證專案功能：

#### 🌐 Web測試工具 (Playwright MCP)
```bash
# 使用Playwright MCP工具測試TradingView圖表
# 1. 啟動API服務
uv run python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000

# 2. 使用Claude Code的瀏覽器工具訪問圖表端點
# 透過MCP Playwright工具可以：
# - 自動截圖圖表輸出
# - 測試互動元素
# - 驗證圖表渲染
# - 檢查響應時間
```

**MCP Playwright功能：**
- `browser_navigate`: 訪問本地API端點
- `browser_snapshot`: 獲取圖表頁面快照  
- `browser_click`: 測試互動元素
- `browser_evaluate`: 執行JavaScript驗證
- `browser_take_screenshot`: 截圖保存測試結果

#### 📊 API端點測試範例
使用MCP瀏覽器工具測試關鍵端點：

```bash
# 1. 健康檢查
http://localhost:8000/health

# 2. 股票分析API
http://localhost:8000/analyze/AAPL

# 3. TradingView自定義圖表
http://localhost:8000/chart/custom/AAPL

# 4. 台股API測試
http://localhost:8000/api/taiwan/market-overview

# 5. 即時WebSocket (需要特殊測試)
ws://localhost:8000/stream/AAPL
```

#### 🔍 自動化測試流程
1. **啟動服務**: 使用`browser_navigate`啟動測試
2. **端點驗證**: 逐一訪問API端點
3. **響應檢查**: 使用`browser_evaluate`檢查JSON響應
4. **圖表測試**: 截圖比較視覺化輸出
5. **錯誤處理**: 測試異常情況

#### 📱 移動端和響應式測試
```bash
# 使用MCP調整瀏覽器視窗大小測試響應式設計
browser_resize(width=375, height=667)  # iPhone視圖
browser_resize(width=768, height=1024) # iPad視圖
browser_resize(width=1920, height=1080) # 桌面視圖
```

#### 🎨 視覺化驗證
- **圖表渲染測試**: 確保K線圖、技術指標正確顯示
- **色彩主題測試**: 驗證暗色/亮色模式
- **數據精確性**: 對比API數據與圖表顯示
- **性能測試**: 測量頁面載入時間

#### ⚡ 實時測試建議
```bash
# 1. 並發測試 - 同時開啟多個標籤頁
browser_tab_new()
browser_tab_select(0)  # AAPL
browser_tab_select(1)  # TSLA
browser_tab_select(2)  # 2330.TW

# 2. 長時間運行測試
browser_wait_for(time=30)  # 等待30秒測試穩定性

# 3. 網路錯誤模擬
# 斷網狀態下測試錯誤處理
```

### 🎯 測試檢查清單
- [ ] ✅ API健康檢查通過
- [ ] ✅ 股票數據獲取正常
- [ ] ✅ 技術指標計算正確
- [ ] ✅ AI分析功能運作
- [ ] ✅ 圖表渲染完整
- [ ] ✅ WebSocket連接穩定
- [ ] ✅ 錯誤處理適當
- [ ] ✅ 性能表現良好

### 🔧 MCP工具使用技巧
1. **批量測試**: 一次開啟多個測試場景
2. **截圖對比**: 保存基準截圖用於迴歸測試
3. **自動化報告**: 結合測試結果生成報告
4. **持續監控**: 定期執行完整測試套件

## 🎯 Next Development Areas

1. **Cloud Deployment**: Terraform scripts (mentioned as "coming soon")
2. **Strategy Comparison**: Interactive comparison tool
3. **Custom Strategy Registration**: Automated strategy factory updates
4. **Monitoring Dashboard**: Prometheus + Grafana integration
5. **Enhanced AI**: More sophisticated recommendation algorithms
6. **MCP Integration**: 深度整合MCP工具用於持續測試和監控