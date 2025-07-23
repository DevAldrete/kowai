"""
Configuration management for KowAI Backend
"""
import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    # Application
    app_name: str = "KowAI Backend"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "default")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Appwrite
    appwrite_endpoint: str = os.getenv("APPWRITE_ENDPOINT", "http://localhost/v1")
    appwrite_project_id: str = os.getenv("APPWRITE_PROJECT_ID", "")
    appwrite_api_key: str = os.getenv("APPWRITE_API_KEY", "")

    # Tool Services
    serper_api_key: str = os.getenv("SERPER_API", "")
    serper_api: str = os.getenv("SERPER_API", "")

    # AI Services
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY", None)
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY", None)
    openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "")
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")

    # Prefect
    prefect_api_url: str = os.getenv("PREFECT_API_URL", "http://localhost:4200/api")

    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # Compression
    compression_enabled: bool | None = os.getenv("COMPRESSION_ENABLED", None)

    compression_level: int | None = os.getenv("COMPRESSION_LEVEL", None)

    # Sequential Processing
    max_concurrent_tasks: int | None = os.getenv("MAX_CONCURRENT_TASKS", None)
    task_timeout_seconds: int | None = os.getenv("TASK_TIMEOUT_SECONDS", None)

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
