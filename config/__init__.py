"""
配置模塊

提供統一的 API 配置管理功能
"""

from .api_config import (
    get_openai_client,
    is_openai_configured,
    get_google_oauth_config,
    is_google_oauth_configured,
    get_database_config,
    get_app_config,
    get_service_status,
    validate_configuration,
    config
)

__all__ = [
    'get_openai_client',
    'is_openai_configured', 
    'get_google_oauth_config',
    'is_google_oauth_configured',
    'get_database_config',
    'get_app_config',
    'get_service_status',
    'validate_configuration',
    'config'
]