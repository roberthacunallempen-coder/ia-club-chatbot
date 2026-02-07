from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List
import os


class Settings(BaseSettings):
    """Application settings and environment variables"""
    
    # Application
    app_name: str = "IA Club Chatbot"
    environment: str = "development"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./chatbot.db"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 800
    
    # Chatwoot
    chatwoot_url: str = ""
    chatwoot_access_token: str = ""
    chatwoot_account_id: int = 0
    chatwoot_inbox_id: int = 0
    chatwoot_webhook_secret: str = ""
    
    # CORS - En producción usar dominios específicos
    allowed_origins: str = "*"
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        if self.allowed_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    # File uploads
    upload_dir: str = "uploads"
    max_file_size: int = 10485760  # 10MB
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    jwt_secret_key: str = "dev-jwt-secret-change-in-production"
    admin_username: str = "admin"
    admin_password: str = "admin123"
    
    # Rate Limiting
    rate_limit_per_minute: int = 30
    rate_limit_per_hour: int = 500
    
    # Logs
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
