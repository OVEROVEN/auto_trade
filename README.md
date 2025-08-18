# AI Trading System

A comprehensive Python-based trading analysis system that combines technical analysis, pattern recognition, and AI-powered insights for stock market analysis.

## Features

### 🚀 Core Capabilities
- **Multi-Market Support**: US stocks (NYSE, NASDAQ) and Taiwan stock market
- **Technical Analysis**: 15+ technical indicators (RSI, MACD, Bollinger Bands, etc.)
- **Pattern Recognition**: Head & Shoulders, Triangles, Double Tops/Bottoms, Breakouts
- **AI Integration**: OpenAI-powered analysis and trading recommendations
- **Real-time Data**: Live market data and WebSocket streaming
- **RESTful API**: FastAPI-based endpoints for all functionality
- **Containerized**: Docker and Docker Compose ready

### 📊 Technical Indicators
- Moving Averages (SMA, EMA)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Stochastic Oscillator
- Williams %R
- ATR (Average True Range)
- ADX (Average Directional Index)
- Volume indicators (OBV, PVT)

### 🎯 Pattern Recognition
- Support and Resistance levels
- Breakout patterns
- Head and Shoulders
- Double Top/Bottom
- Triangle patterns (Ascending, Descending, Symmetrical)
- Flag and Pennant patterns

### 🤖 AI Analysis
- Technical data analysis using GPT-4
- Chart image analysis with GPT-4 Vision
- Market sentiment analysis
- Automated trading strategy generation

## Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API key (for AI features)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone and setup**:
```bash
git clone <repository-url>
cd auto_trade
cp .env.example .env
```

2. **Configure environment variables**:
Edit `.env` file with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_PASSWORD=secure_password
REDIS_PASSWORD=redis_password
```

3. **Start the system**:
```bash
# Production environment
docker-compose up -d

# Development environment
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

4. **Access the API**:
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- PgAdmin (dev): http://localhost:5050

### Local Development

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set environment variables**:
```bash
export OPENAI_API_KEY="your_key_here"
export DATABASE_URL="postgresql://user:pass@localhost:5432/trading_db"
```

3. **Run the application**:
```bash
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Usage Examples

### Analyze a Stock
```bash
curl -X POST "http://localhost:8000/analyze/AAPL" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "period": "3mo",
    "include_ai": true,
    "include_patterns": true
  }'
```

### Get Trading Signals
```bash
curl "http://localhost:8000/signals/AAPL"
```

### Detect Patterns
```bash
curl "http://localhost:8000/patterns/TSLA"
```

### WebSocket Stream (JavaScript)
```javascript
const ws = new WebSocket('ws://localhost:8000/stream/AAPL');
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Real-time update:', data);
};
```

## Supported Symbols

### US Market
- AAPL (Apple)
- GOOGL (Google)
- TSLA (Tesla)
- SPY (S&P 500 ETF)
- QQQ (NASDAQ ETF)
- And any valid US stock symbol

### Taiwan Market
- 2330.TW (TSMC)
- 2317.TW (Hon Hai)
- 0050.TW (Taiwan 50 ETF)
- And any valid Taiwan stock symbol

## Configuration

### Environment Variables
Key configuration options in `.env`:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key
ALPHA_VANTAGE_API_KEY=optional_alpha_vantage_key

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/trading_db
DATABASE_PASSWORD=secure_password

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=redis_password

# Trading Settings
DEFAULT_STOP_LOSS=0.02
DEFAULT_POSITION_SIZE=0.1
UPDATE_INTERVAL_MINUTES=15

# Application
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
```

### Trading Parameters
Customize trading analysis in `config/settings.py`:
- Technical indicator periods
- Pattern recognition sensitivity
- Risk management settings
- AI analysis parameters

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   Data Fetchers │    │   Analyzers     │
│   REST API      │◄───┤   - US Stocks   │◄───┤   - Technical   │
│   WebSocket     │    │   - TW Stocks   │    │   - Patterns    │
└─────────────────┘    └─────────────────┘    │   - AI Analysis │
         │                                     └─────────────────┘
         ▼                                              │
┌─────────────────┐    ┌─────────────────┐             │
│   PostgreSQL    │    │     Redis       │             │
│   (TimescaleDB) │    │    (Cache)      │             │
└─────────────────┘    └─────────────────┘             │
         ▲                                              │
         └──────────────────────────────────────────────┘
```

## Development

### Project Structure
```
trading-system/
├── src/
│   ├── data_fetcher/       # Market data collection
│   ├── analysis/           # Technical & AI analysis
│   ├── strategy/           # Trading strategies
│   ├── backtesting/        # Strategy backtesting
│   └── api/               # FastAPI application
├── config/                # Configuration management
├── tests/                 # Test suite
├── docker-compose.yml     # Production deployment
├── docker-compose.dev.yml # Development environment
└── requirements.txt       # Python dependencies
```

### Running Tests
```bash
# Unit tests
pytest tests/

# Integration tests
pytest tests/integration/

# With coverage
pytest --cov=src tests/
```

### Adding New Features

1. **New Technical Indicator**:
   - Add function to `src/analysis/technical_indicators.py`
   - Update `IndicatorAnalyzer.calculate_all_indicators()`

2. **New Pattern**:
   - Add detection method to `src/analysis/pattern_recognition.py`
   - Update `PatternRecognition.analyze_all_patterns()`

3. **New Data Source**:
   - Create new fetcher in `src/data_fetcher/`
   - Update API endpoints to support new source

## Deployment

### Production Deployment
```bash
# Build and deploy
docker-compose -f docker-compose.yml --profile production up -d

# With monitoring
docker-compose -f docker-compose.yml --profile production --profile monitoring up -d
```

### Cloud Deployment (AWS)
1. Set up ECS cluster
2. Configure RDS PostgreSQL
3. Deploy using provided Terraform scripts (coming soon)

### Environment-Specific Configs
- **Development**: Hot reloading, debug logs, dev databases
- **Production**: Optimized builds, health checks, monitoring
- **Testing**: Isolated databases, mocked external APIs

## Monitoring and Logging

### Health Checks
- Application: `/health`
- Database connectivity
- External API availability
- Market status monitoring

### Logging
- Structured JSON logging
- Configurable log levels
- Separate logs for different components
- Error tracking and alerting

### Monitoring (Optional)
- Prometheus metrics collection
- Grafana dashboards
- Performance monitoring
- Alert management

## API Documentation

Full API documentation is available at `/docs` when running the application.

### Key Endpoints
- `POST /analyze/{symbol}` - Comprehensive stock analysis
- `GET /signals/{symbol}` - Trading signals
- `GET /patterns/{symbol}` - Detected patterns
- `GET /symbols` - Available symbols
- `WS /stream/{symbol}` - Real-time updates

## Troubleshooting

### Common Issues

1. **OpenAI API Errors**:
   - Verify API key is set correctly
   - Check API quota and billing
   - Review rate limiting

2. **Data Fetching Issues**:
   - Check internet connectivity
   - Verify symbol format (e.g., "2330.TW" for Taiwan stocks)
   - Review market hours

3. **Docker Issues**:
   - Ensure Docker daemon is running
   - Check port availability
   - Review container logs: `docker-compose logs trading_app`

### Performance Optimization
- Use Redis caching for frequent requests
- Implement connection pooling for databases
- Optimize data fetching batch sizes
- Monitor memory usage for large datasets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Your License Here]

## Disclaimer

This software is for educational and research purposes only. It does not constitute financial advice. Always consult with qualified financial advisors before making investment decisions.

## Support

For issues and questions:
- Check the documentation
- Review common troubleshooting steps
- Open an issue on GitHub
- Check the API health endpoint for system status