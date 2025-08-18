from typing import Optional
from pydantic import BaseSettings, Field
import os
from pathlib import Path

class Settings(BaseSettings):
    # API Keys
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    alpha_vantage_api_key: Optional[str] = Field(None, env="ALPHA_VANTAGE_API_KEY")
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    
    # Database Configuration
    database_url: str = Field(..., env="DATABASE_URL")
    database_host: str = Field("localhost", env="DATABASE_HOST")
    database_port: int = Field(5432, env="DATABASE_PORT")
    database_name: str = Field("trading_db", env="DATABASE_NAME")
    database_user: str = Field("trading_user", env="DATABASE_USER")
    database_password: str = Field(..., env="DATABASE_PASSWORD")
    
    # Redis Configuration
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    redis_db: int = Field(0, env="REDIS_DB")
    
    # Trading Configuration
    default_stop_loss: float = Field(0.02, env="DEFAULT_STOP_LOSS")
    default_position_size: float = Field(0.1, env="DEFAULT_POSITION_SIZE")
    risk_free_rate: float = Field(0.045, env="RISK_FREE_RATE")
    
    # Market Data Configuration
    update_interval_minutes: int = Field(15, env="UPDATE_INTERVAL_MINUTES")
    max_symbols_per_batch: int = Field(10, env="MAX_SYMBOLS_PER_BATCH")
    
    # TradingView Configuration
    tradingview_username: Optional[str] = Field(None, env="TRADINGVIEW_USERNAME")
    tradingview_password: Optional[str] = Field(None, env="TRADINGVIEW_PASSWORD")
    
    # Taiwan Stock Market
    twse_api_key: Optional[str] = Field(None, env="TWSE_API_KEY")
    
    # FastAPI Configuration
    api_host: str = Field("0.0.0.0", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")
    api_workers: int = Field(4, env="API_WORKERS")
    
    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("logs/trading_system.log", env="LOG_FILE")
    
    # Cloud Configuration (AWS)
    aws_region: str = Field("us-east-1", env="AWS_REGION")
    aws_access_key_id: Optional[str] = Field(None, env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(None, env="AWS_SECRET_ACCESS_KEY")
    s3_bucket_name: Optional[str] = Field(None, env="S3_BUCKET_NAME")
    
    # Cloud Configuration (Azure)
    azure_storage_connection_string: Optional[str] = Field(None, env="AZURE_STORAGE_CONNECTION_STRING")
    azure_container_name: Optional[str] = Field(None, env="AZURE_CONTAINER_NAME")
    
    # Development/Production
    environment: str = Field("development", env="ENVIRONMENT")
    debug: bool = Field(True, env="DEBUG")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Create a global settings instance
settings = Settings()

# US Market symbols for initial testing
US_SYMBOLS = [
    "AAPL",   # Apple
    "GOOGL",  # Google
    "TSLA",   # Tesla
    "SPY",    # S&P 500 ETF
    "QQQ",    # NASDAQ ETF
    "MSFT",   # Microsoft
    "AMZN",   # Amazon
    "NVDA",   # NVIDIA
]

# Taiwan Market symbols
TW_SYMBOLS = [
    "2330.TW",  # TSMC
    "2317.TW",  # Hon Hai
    "0050.TW",  # Taiwan 50 ETF
    "2454.TW",  # MediaTek
    "2881.TW",  # Fubon Financial
]

# Technical indicator periods
TECHNICAL_PERIODS = {
    "rsi": 14,
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,
    "bb_period": 20,
    "bb_std": 2,
    "sma_short": 20,
    "sma_long": 50,
    "ema_short": 12,
    "ema_long": 26,
}

# Pattern recognition parameters
PATTERN_CONFIG = {
    "min_pattern_length": 10,
    "max_pattern_length": 50,
    "volume_spike_threshold": 1.5,
    "breakout_volume_multiplier": 1.2,
    "support_resistance_touches": 3,
}

# Risk management settings
RISK_MANAGEMENT = {
    "max_portfolio_risk": 0.02,  # 2% of portfolio per trade
    "max_correlation": 0.7,      # Maximum correlation between positions
    "max_sector_exposure": 0.3,  # Maximum 30% in any sector
    "rebalance_threshold": 0.05, # Rebalance when allocation drifts 5%
}

def get_database_url() -> str:
    """Get the formatted database URL for SQLAlchemy."""
    return f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

def get_log_dir() -> Path:
    """Ensure log directory exists and return path."""
    log_path = Path(settings.log_file).parent
    log_path.mkdir(parents=True, exist_ok=True)
    return log_path