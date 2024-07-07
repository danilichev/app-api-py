import os

from pydantic import RedisDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    db_host: str = os.getenv("DB_HOST")
    db_name: str = os.getenv("DB_NAME")
    db_password: str = os.getenv("DB_PASSWORD")
    db_port: int = os.getenv("DB_PORT", 5432)
    db_user: str = os.getenv("DB_USER")
    environment: str = os.getenv("ENVIRONMENT", "development")
    redis_db: str = os.getenv("REDIS_DB", "0")
    redis_host: str = os.getenv("REDIS_HOST")
    redis_port: int = os.getenv("REDIS_PORT", 6379)

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def redis_url(self) -> RedisDsn:
        return MultiHostUrl.build(
            host=self.redis_host,
            path=self.redis_db,
            port=self.redis_port,
            scheme="redis",
        )


config = Config()
