"""Configuration management for FastAPI application"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # FastAPI Settings
    FASTAPI_ENV: str = "development"
    DEBUG: bool = False

    # JWT Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 15
    JWT_REFRESH_EXPIRATION_DAYS: int = 7

    # CosmosDB Settings
    COSMOSDB_ENDPOINT: str = "https://localhost:8081"
    COSMOSDB_KEY: str = "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDL5NxcwooEV3TqQ=="
    COSMOSDB_DATABASE: str = "pianotracker"

    # CORS Settings
    CORS_ORIGINS: Optional[str] = "http://localhost:3000"

    # Logging Settings
    LOG_LEVEL: str = "INFO"

    class Config:
        """Pydantic settings configuration"""
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True
