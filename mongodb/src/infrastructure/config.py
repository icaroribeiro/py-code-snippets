from functools import cache
from pathlib import Path

from pydantic import Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.logging.logger_factory import get_logger

logger = get_logger(__name__)


class I18nSettings(BaseSettings):
    model_config = SettingsConfigDict(  # type: ignore
        env_file=".env",
        env_prefix="I18N_",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_extra=True,
    )

    path_to_files: Path = Field(default=Path("your_i18n_path_to_files_here"))

    @field_validator("path_to_files", mode="after")
    @classmethod
    def resolve_to_absolute_path(cls, v: Path) -> Path:
        """
        Forces the path to be absolute, resolving it based on the
        current working directory execution context.
        """
        absolute_path = v.resolve()

        # Optional: Adds a warning log or validation error if you want to catch misconfigurations early
        if not absolute_path.exists():
            logger.info(
                f"[WARNING] i18n directory source not found at: {absolute_path}"
            )

        return absolute_path


class MongoDBSettings(BaseSettings):
    model_config = SettingsConfigDict(  # type: ignore
        env_file=".env",
        env_prefix="MONGODB_",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_extra=True,
    )

    username: str = Field(default="your_mongodb_username_here")
    password: str = Field(default="your_mongodb_password_here")
    host: str = Field(default="your_mongodb_host_here")
    port: int = Field(default=0)
    database: str = Field(default="your_mongodb_database_name_here")
    migrations_path: Path = Field(
        default=Path("your_mongodb_path_to_migrations_here")
    )
    conn_string: str | None = Field(default=None)

    @field_validator("migrations_path", mode="after")
    @classmethod
    def resolve_migrations_path(cls, v: Path) -> Path:
        """
        Resolves the relative migrations path to an absolute system path early.
        """
        absolute_path = v.resolve()
        if not absolute_path.exists():
            logger.info(
                f"[WARNING] MongoDB migrations directory not found at: {absolute_path}"
            )
        return absolute_path

    @computed_field
    @property
    def uri(self) -> str:
        if self.conn_string:
            return self.conn_string
        uri = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}"
        return uri


@cache
def get_i18n_settings() -> I18nSettings:
    return I18nSettings()


@cache
def get_mongodb_settings() -> MongoDBSettings:
    return MongoDBSettings()
