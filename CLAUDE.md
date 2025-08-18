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

## 🎯 Next Development Areas

1. **Cloud Deployment**: Terraform scripts (mentioned as "coming soon")
2. **Strategy Comparison**: Interactive comparison tool
3. **Custom Strategy Registration**: Automated strategy factory updates
4. **Monitoring Dashboard**: Prometheus + Grafana integration
5. **Enhanced AI**: More sophisticated recommendation algorithms