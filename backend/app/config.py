"""
AI Agent Backend - Configuration Management

Handles environment variables, database connections, and model initialization.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "AI Agent System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, validation_alias="DEBUG")
    ENVIRONMENT: str = Field(default="development", validation_alias="ENVIRONMENT")
    
    # Server
    HOST: str = Field(default="0.0.0.0", validation_alias="HOST")
    PORT: int = Field(default=8000, validation_alias="PORT")
    
    # OpenRouter LLM
    OPENROUTER_API_KEY: str = Field(validation_alias="OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL: str = Field(
        default="https://openrouter.ai/api/v1",
        validation_alias="OPENROUTER_BASE_URL"
    )
    LLM_MODEL: str = Field(default="mistralai/mistral-7b-instruct", validation_alias="LLM_MODEL")
    
    # Database
    DATABASE_URL: str = Field(validation_alias="DATABASE_URL")
    DATABASE_POOL_SIZE: int = Field(default=20, validation_alias="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=10, validation_alias="DATABASE_MAX_OVERFLOW")
    
    # Vector Database (Qdrant)
    QDRANT_URL: str = Field(validation_alias="QDRANT_URL")
    QDRANT_API_KEY: Optional[str] = Field(default=None, validation_alias="QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: str = Field(default="agent_memory", validation_alias="QDRANT_COLLECTION_NAME")
    
    # Embeddings
    EMBEDDING_MODEL: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        validation_alias="EMBEDDING_MODEL"
    )
    EMBEDDING_DIMENSION: int = Field(default=384, validation_alias="EMBEDDING_DIMENSION")
    
    # Agent Configuration
    MAX_ITERATIONS: int = Field(default=10, validation_alias="MAX_ITERATIONS")
    TIMEOUT_SECONDS: int = Field(default=300, validation_alias="TIMEOUT_SECONDS")
    MEMORY_RETENTION_DAYS: int = Field(default=30, validation_alias="MEMORY_RETENTION_DAYS")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        validation_alias="LOG_FORMAT"
    )
    
    # CORS
    CORS_ORIGINS: list = Field(default=["*"], validation_alias="CORS_ORIGINS")
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, validation_alias="CORS_ALLOW_CREDENTIALS")
    CORS_ALLOW_METHODS: list = Field(default=["*"], validation_alias="CORS_ALLOW_METHODS")
    CORS_ALLOW_HEADERS: list = Field(default=["*"], validation_alias="CORS_ALLOW_HEADERS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Singleton instance
settings = Settings()
