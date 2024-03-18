import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
    db_host: str = os.getenv("DB_HOST")
    db_port: int = os.getenv("DB_PORT", 5432)
    db_name: str = os.getenv("DB_NAME")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    environment: str = "development"

    model_config = SettingsConfigDict(env_file=".env")


config = Config()
