from functools import lru_cache
from pydantic import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()  # Isso garante que as variáveis do .env sejam carregadas


class Settings(BaseSettings):
    app_name: str = "Fastapi Base"
    app_alias: str = "fastapi_base"
    version: str = "1.0.0"
    app_env: str = "development"
    api_key: str = "api-key"
    username_docs: str = "fastapi_base"
    password_docs: str = "fastapi_base_pass"
    log_level: str = "INFO"

    database_url: str = os.getenv("DATABASE_URL", "")
    database_pool_size: int = 10
    database_pool_overflow: int = 5

    prefix_url_path: str = ""
    redis_url: str = os.getenv("REDIS_URL", "redis://redis/0")

    rabbit_url: str = os.getenv("RABBIT_URL", "pyamqp://guest:guest@rabbitmq:5672//")
    rabbit_default_exchange: str = "amq.topic"
    rabbit_default_queue: str = "celery"

    class Config:
        env_file = ".env"  # Define o caminho para o arquivo .env


@lru_cache()
def get_settings() -> Settings:
    """Get settings from environment."""
    return Settings()
