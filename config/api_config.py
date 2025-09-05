"""
🔧 API 配置統一管理模塊

這個模塊負責集中管理所有外部服務的 API 配置，
包括 OpenAI、Google OAuth、資料庫連接等。

使用方式：
    from config.api_config import get_openai_client, get_google_oauth_config
    
    # 獲取 OpenAI 客戶端
    openai_client = get_openai_client()
    
    # 檢查服務可用性
    if is_openai_configured():
        # 使用 AI 功能
"""

import os
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

# 設置日誌
logger = logging.getLogger(__name__)

@dataclass
class OpenAIConfig:
    """OpenAI 服務配置"""
    api_key: Optional[str]
    model: str = "gpt-4o"  # 預設使用最新的 GPT-4o 模型
    max_tokens: int = 2000
    temperature: float = 0.3
    timeout: int = 30

@dataclass
class GoogleOAuthConfig:
    """Google OAuth 配置"""
    client_id: Optional[str]
    client_secret: Optional[str]
    redirect_uri: str = "http://localhost:8080/api/auth/google/callback"

@dataclass
class DatabaseConfig:
    """資料庫配置"""
    url: str = "sqlite:///trading.db"
    echo: bool = False

@dataclass
class AppConfig:
    """應用程式全域配置"""
    environment: str = "development"
    debug: bool = True
    port: int = 8080
    cors_origins: list = None
    jwt_secret: str = "your-secret-key-here-change-in-production"
    
    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = [
                "http://localhost:3000",
                "http://127.0.0.1:3000"
            ]

class APIConfigManager:
    """API 配置管理器"""
    
    def __init__(self):
        self._load_from_environment()
    
    def _load_from_environment(self):
        """從環境變數載入配置"""
        # OpenAI 配置
        self.openai = OpenAIConfig(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "2000")),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.3")),
            timeout=int(os.getenv("OPENAI_TIMEOUT", "30"))
        )
        
        # Google OAuth 配置
        self.google_oauth = GoogleOAuthConfig(
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
            redirect_uri=os.getenv("GOOGLE_REDIRECT_URI", 
                                  "http://localhost:8080/api/auth/google/callback")
        )
        
        # 資料庫配置
        self.database = DatabaseConfig(
            url=os.getenv("DATABASE_URL", "sqlite:///trading.db"),
            echo=os.getenv("DEBUG", "false").lower() == "true"
        )
        
        # 應用程式配置
        cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
        cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]
        
        self.app = AppConfig(
            environment=os.getenv("ENVIRONMENT", "development"),
            debug=os.getenv("DEBUG", "true").lower() == "true",
            port=int(os.getenv("PORT", "8080")),
            cors_origins=cors_origins,
            jwt_secret=os.getenv("JWT_SECRET", "your-secret-key-here-change-in-production")
        )
    
    def is_openai_configured(self) -> bool:
        """檢查 OpenAI 是否已正確配置"""
        return bool(self.openai.api_key and self.openai.api_key.startswith('sk-'))
    
    def is_google_oauth_configured(self) -> bool:
        """檢查 Google OAuth 是否已正確配置"""
        return bool(self.google_oauth.client_id and self.google_oauth.client_secret)
    
    def get_service_status(self) -> Dict[str, Any]:
        """獲取所有服務配置狀態"""
        return {
            "openai": {
                "configured": self.is_openai_configured(),
                "model": self.openai.model,
                "api_key_preview": f"{self.openai.api_key[:8]}..." if self.openai.api_key else None
            },
            "google_oauth": {
                "configured": self.is_google_oauth_configured(),
                "client_id_preview": f"{self.google_oauth.client_id[:12]}..." if self.google_oauth.client_id else None
            },
            "database": {
                "url": self.database.url,
                "type": "sqlite" if "sqlite" in self.database.url else "postgresql"
            },
            "app": {
                "environment": self.app.environment,
                "debug": self.app.debug,
                "port": self.app.port
            }
        }

# 全域配置實例
config = APIConfigManager()

def get_openai_client():
    """
    獲取配置好的 OpenAI 客戶端
    
    Returns:
        openai.OpenAI: 配置好的 OpenAI 客戶端
        
    Raises:
        ValueError: 如果 OpenAI API key 未配置
    """
    if not config.is_openai_configured():
        raise ValueError(
            "OpenAI API key 未配置。請在環境變數中設置 OPENAI_API_KEY，"
            "或參考 .env.example 檔案進行配置。"
        )
    
    try:
        import openai
        client = openai.OpenAI(
            api_key=config.openai.api_key,
            timeout=config.openai.timeout
        )
        logger.info(f"OpenAI 客戶端已初始化 (model: {config.openai.model})")
        return client
    except ImportError:
        raise ImportError("請安裝 openai 套件: pip install openai")

def is_openai_configured() -> bool:
    """檢查 OpenAI 是否已配置"""
    return config.is_openai_configured()

def get_google_oauth_config() -> GoogleOAuthConfig:
    """獲取 Google OAuth 配置"""
    return config.google_oauth

def is_google_oauth_configured() -> bool:
    """檢查 Google OAuth 是否已配置"""
    return config.is_google_oauth_configured()

def get_database_config() -> DatabaseConfig:
    """獲取資料庫配置"""
    return config.database

def get_app_config() -> AppConfig:
    """獲取應用程式配置"""
    return config.app

def get_service_status() -> Dict[str, Any]:
    """獲取所有服務配置狀態"""
    return config.get_service_status()

def validate_configuration():
    """
    驗證關鍵配置項目
    
    Returns:
        Dict[str, Any]: 驗證結果
    """
    issues = []
    warnings = []
    
    # 檢查 OpenAI 配置
    if not is_openai_configured():
        warnings.append("OpenAI API key 未配置，AI 功能將不可用")
    
    # 檢查 Google OAuth 配置
    if not is_google_oauth_configured():
        warnings.append("Google OAuth 未完整配置，社交登入將不可用")
    
    # 檢查 JWT secret
    if config.app.jwt_secret == "your-secret-key-here-change-in-production":
        issues.append("JWT secret 仍使用預設值，請在生產環境中更改")
    
    # 檢查生產環境配置
    if config.app.environment == "production":
        if config.app.debug:
            issues.append("生產環境不應啟用 debug 模式")
        
        if "localhost" in str(config.google_oauth.redirect_uri):
            issues.append("生產環境的 Google OAuth redirect URI 不應使用 localhost")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "status": get_service_status()
    }

# 模塊初始化時的配置檢查
if __name__ == "__main__":
    validation = validate_configuration()
    print("🔧 API 配置檢查結果:")
    print(f"✅ 配置有效: {validation['valid']}")
    
    if validation['issues']:
        print("\n❌ 發現問題:")
        for issue in validation['issues']:
            print(f"  - {issue}")
    
    if validation['warnings']:
        print("\n⚠️  警告:")
        for warning in validation['warnings']:
            print(f"  - {warning}")
    
    print(f"\n📊 服務狀態:")
    for service, status in validation['status'].items():
        print(f"  {service}: {status}")