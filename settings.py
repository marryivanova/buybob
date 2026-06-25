import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class DatabaseSettings(BaseSettings):
    host: str = os.getenv("DB_HOST")
    port: str = os.getenv("DB_PORT")
    user: str = os.getenv("DB_USER")
    password: str = os.getenv("DB_PASSWORD")
    database: str = os.getenv("DB_NAME")


class AppSettings(BaseSettings):
    host: str = os.getenv("APP_HOST")
    port: str = os.getenv("APP_PORT")


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    app: AppSettings = AppSettings()


settings = Settings()
