from functools import lru_cache
from typing import Literal

from pydantic import SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_DEFAULT_JWT_SECRET = "change-me"


class Settings(BaseSettings):
    """Конфигурация из переменных окружения. Секретов в коде нет."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: Literal["development", "test", "production"] = "development"
    log_level: str = "INFO"

    database_url: str = "postgresql+asyncpg://nftscanner:nftscanner@localhost:5432/nftscanner"

    jwt_secret: SecretStr = SecretStr(_DEFAULT_JWT_SECRET)
    telegram_bot_token: SecretStr = SecretStr("")

    cors_origins: list[str] = ["http://localhost:3000"]

    scanner_mode: Literal["demo", "real"] = "demo"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: object) -> object:
        # Разрешаем формат "a,b" в .env вместо JSON-списка.
        if isinstance(value, str) and not value.strip().startswith("["):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @model_validator(mode="after")
    def _check_production(self) -> "Settings":
        if self.app_env == "production":
            if self.jwt_secret.get_secret_value() == _DEFAULT_JWT_SECRET:
                raise ValueError("JWT_SECRET must be set in production")
            if "*" in self.cors_origins:
                raise ValueError("Wildcard CORS is not allowed in production")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
