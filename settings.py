import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class DatabaseSettings(BaseSettings):
    host: str = os.getenv("DB_HOST", "localhost")
    port: str = os.getenv("DB_PORT", "5432")
    user: str = os.getenv("DB_USER", "postgres")
    password: str = os.getenv("DB_PASSWORD", "postgres")
    database: str = os.getenv("DB_NAME", "contest")

    @property
    def db_url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class AppSettings(BaseSettings):
    host: str = os.getenv("APP_HOST", "localhost")
    port: str = os.getenv("APP_PORT", "8000")


class RedisSettings(BaseSettings):
    password: str = os.getenv("REDIS_PASSWORD", "skogbjbbrt43t8tu34838")
    username: str = os.getenv("REDIS_USERNAME", "redis")
    user_password: str = os.getenv("REDIS_PASSWORD", "skogbjbbrt43t8tu34838")
    host: str = os.getenv("REDIS_HOST", "localhost")
    port: str = os.getenv("REDIS_PORT", "6379")


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    app: AppSettings = AppSettings()


TORTOISE_ORM = {
    "connections": {"default": "postgres://postgres:postgres@localhost:5432/contest"},
    "apps": {
        "models": {
            "models": ["app.admin.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

settings = Settings()
