from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings
from functools import lru_cache
import os
import yaml

class Settings(BaseSettings):
    # Base project configuration
    PROJECT_NAME: str = "AI Demo"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # Database configuration
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "ai_demo"
    DATABASE_URL: Optional[str] = None

    # JWT configuration
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS configuration
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]

    # Default superuser
    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"
    FIRST_SUPERUSER_EMAIL: str = "admin@example.com"

    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # If DATABASE_URL is not set, build it from components
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )

class ConfigManager:
    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        """Load configuration files"""
        # Get config path from environment variable, or use default path
        config_path = os.getenv('CONFIG_PATH', 'backend/config/default.yaml')
        
        # If environment is specified, load corresponding config file
        env = os.getenv('ENV', 'default')
        env_config_path = f'backend/config/{env}.yaml'

        # Load default configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)

        # If environment-specific config exists, override default settings
        if os.path.exists(env_config_path) and env != 'default':
            with open(env_config_path, 'r', encoding='utf-8') as f:
                env_config = yaml.safe_load(f)
                self._deep_update(self._config, env_config)

    def _deep_update(self, base_dict: dict, update_dict: dict):
        """Recursively update dictionary"""
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value

    @property
    def database_url(self) -> str:
        """Build database URL from configuration"""
        db = self._config['database']
        return f"{db['type']}://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['db_name']}"

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        try:
            keys = key.split('.')
            value = self._config
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def __getitem__(self, key: str) -> Any:
        """Access configuration using dictionary style"""
        return self.get(key)

@lru_cache()
def get_settings() -> ConfigManager:
    """Get configuration manager singleton"""
    return ConfigManager()

# Create global settings instance
settings = get_settings() 