from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    host: str = Field("localhost", validation_alias="DB_HOST")
    port: int = Field(5432, validation_alias="DB_PORT")
    user: str = Field("postgres", validation_alias="DB_USER")
    password: str = Field("postgres", validation_alias="DB_PASSWORD")
    database: str = Field("contest", validation_alias="DB_NAME")

    @property
    def db_url(self) -> str:
        return f"postgres://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class AppSettings(BaseSettings):
    host: str = Field("0.0.0.0", validation_alias="APP_HOST")
    port: int | str = Field(8000, validation_alias="APP_PORT")


class RedisSettings(BaseSettings):
    host: str = Field("localhost", validation_alias="REDIS_HOST")
    port: int = Field(6379, validation_alias="REDIS_PORT")
    username: str = Field("redis", validation_alias="REDIS_USERNAME")
    password: str = Field("password", validation_alias="REDIS_PASSWORD")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    app: AppSettings = AppSettings()


settings = Settings()
