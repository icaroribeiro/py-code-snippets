from enum import Enum
from functools import cache
from pathlib import Path
from typing import Any

from pydantic import Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from infrastructure.cross_cutting.logging import get_logger

logger = get_logger(__name__)


class HTTPServerSettings(BaseSettings):
    model_config = SettingsConfigDict(  # type: ignore
        env_file=".env",
        env_prefix="HTTP_SERVER_",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_extra=True,
        case_sensitive=False,
    )

    host: str = Field(default="your_http_server_host_here")
    port: int = Field(default=0)
    env: str = Field(default="your_http_server_environment_here")

    @property
    def is_development(self) -> bool:
        return self.env.lower() in {"development", "dev", "local"}

    @property
    def is_production(self) -> bool:
        return self.env.lower() in {"production", "prod"}

class HTTPClientSettings(BaseSettings):
    model_config = SettingsConfigDict(  # type: ignore
        env_file=".env",
        env_prefix="HTTP_CLIENT",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_extra=True,
        case_sensitive=False,
    )

    timeout_seconds: float = Field(default=0)

class MongoDBSettings(BaseSettings):
    model_config = SettingsConfigDict(  # type: ignore
        env_file=".env",
        env_prefix="MONGODB_",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_extra=True,
        case_sensitive=False,
    )

    username: str = Field(default="your_mongodb_username_here")
    password: str = Field(default="your_mongodb_password_here")
    host: str = Field(default="your_mongodb_host_here")
    port: int = Field(default=0)
    database: str = Field(default="your_mongodb_database_name_here")
    migrations_path: Path = Field(default=Path("infrastructure/mongodb/migrations"))
    conn_string: str | None = Field(default=None)

    @field_validator("migrations_path", mode="after")
    @classmethod
    def resolve_migrations_path(cls, v: Path) -> Path:
        absolute_path = v.resolve()
        if not absolute_path.exists():
            logger.info(
                f"[WARNING] MongoDB migrations directory not found at: {absolute_path}"
            )
        return absolute_path

    @computed_field
    @property
    def uri(self) -> str:
        if self.conn_string and self.conn_string != "":
            return self.conn_string
        uri = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}"
        return uri


class TelegramMode(str, Enum):
    POLLING = "polling"
    WEBHOOK = "webhook"


class TelegramSettings(BaseSettings):
    model_config = SettingsConfigDict(  # type: ignore
        env_file=".env",
        env_prefix="TELEGRAM_",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_extra=True,
        case_sensitive=False,
    )

    mode: TelegramMode = Field(default=TelegramMode.POLLING)
    bot_token: str = Field(default="your_bot_token_here")
    api_secret: str = Field(default="your_api_secret_here")


    @field_validator("mode", mode="before")
    @classmethod
    def normalize_mode_to_lowercase(cls, v: Any) -> str:
        """
        Intercepts the incoming value for 'mode' and normalizes it to lowercase
        to ensure seamless Enum alignment, whether it comes as 'WEBHOOK' or 'webhook'.
        """
        if isinstance(v, str):
            normalized = v.strip().lower()
            logger.debug(f"Normalizing Telegram mode incoming value from '{v}' to '{normalized}'")
            return normalized
        return v

@cache
def get_http_server_settings() -> HTTPServerSettings:
    return HTTPServerSettings()


@cache
def get_telegram_settings() -> TelegramSettings:
    return TelegramSettings()


@cache
def get_mongodb_settings() -> MongoDBSettings:
    return MongoDBSettings()
