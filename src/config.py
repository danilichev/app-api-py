import os

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
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM")
    jwt_expire: int = os.getenv("JWT_EXPIRE", 3600)
    mivolo_checkpoints_path: str = os.getenv("MIVOLO_CHECKPOINTS_PATH")
    redis_db: str = os.getenv("REDIS_DB", "0")
    redis_host: str = os.getenv("REDIS_HOST")
    redis_port: int = os.getenv("REDIS_PORT", 6379)
    temp_dir: str = os.getenv("TEMP_DIR", "temp")

    @property
    def db_url(self) -> str:
        return MultiHostUrl.build(
            host=self.db_host,
            path=self.db_name,
            port=self.db_port,
            scheme="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_password,
        ).unicode_string()

    @property
    def redis_url(self) -> str:
        return MultiHostUrl.build(
            host=self.redis_host,
            path=self.redis_db,
            port=self.redis_port,
            scheme="redis",
        ).unicode_string()


config = Config()

print("path", config.mivolo_checkpoints_path)
