import os
from pathlib import Path
from functools import lru_cache
from typing import List

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseModel):
    """数据库配置"""
    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    user: str = Field(default="postgres")
    password: str = Field(default="postgres")
    db: str = Field(default="ai_demo")

class Settings(BaseSettings):
    """应用配置"""
    # 环境
    ENV: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    
    # 数据库配置
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_DB: str = Field(default="ai_demo")
    
    # Flask 配置
    SECRET_KEY: str = Field(default="ai-demo-secret-key-2024-01-01")
    SESSION_COOKIE_SECURE: bool = Field(default=True)
    SESSION_COOKIE_HTTPONLY: bool = Field(default=True)
    PERMANENT_SESSION_LIFETIME: int = Field(default=3600)  # 1小时
    
    # JWT 配置
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)
    
    # CORS 配置
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"])
    CORS_CREDENTIALS: bool = Field(default=True)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    @property
    def DATABASE_URL(self) -> str:
        """获取数据库 URL"""
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """获取同步数据库 URL（用于 Flask-SQLAlchemy）"""
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def IS_DEVELOPMENT(self) -> bool:
        """是否为开发环境"""
        return self.ENV.lower() == "development"
    
    @property
    def IS_PRODUCTION(self) -> bool:
        """是否为生产环境"""
        return self.ENV.lower() == "production"
    
    @property
    def IS_TESTING(self) -> bool:
        """是否为测试环境"""
        return self.ENV.lower() == "testing"

@lru_cache
def get_settings() -> Settings:
    """获取应用配置（使用缓存）"""
    return Settings()

settings = get_settings() 