from functools import cache
from pathlib import Path

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


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(  # type: ignore
        env_file=".env",
        env_prefix="REDIS_",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_extra=True,
        case_sensitive=False,
    )

    password: str | None = Field(default=None)
    host: str = Field(default="your_redis_host_here")
    port: int = Field(default=0)

    # Separation of logical databases inside Redis
    rate_limit_db: int = Field(default=0)
    rate_limit_conn_string: str | None = Field(default=None)

    backend_db: int = Field(
        default=1
    )  # Changed default to 1 to segregate from rate limit
    backend_conn_string: str | None = Field(default=None)

    @computed_field
    @property
    def rate_limit_url(self) -> str:
        if self.rate_limit_conn_string:
            return self.rate_limit_conn_string
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.rate_limit_db}"

    @computed_field
    @property
    def backend_url(self) -> str:
        if self.backend_conn_string:
            return self.backend_conn_string
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.backend_db}"


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(  # type: ignore
        env_file=".env",
        env_prefix="RABBITMQ_",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_extra=True,
        case_sensitive=False,
    )

    username: str = Field(default="your_rabbitmq_username_here")
    password: str = Field(default="your_rabbitmq_password_here")
    host: str = Field(default="your_rabbitmq_host_here")
    port: int = Field(default=0)
    vhost: str = Field(
        default=""
    )  # RabbitMQ virtual host string (empty defaults to '/')

    conn_string: str | None = Field(default=None)

    @computed_field
    @property
    def url(self) -> str:
        if self.conn_string:
            return self.conn_string

        auth = f"{self.username}:{self.password}@"
        return f"amqp://{auth}{self.host}:{self.port}/{self.vhost}"


class CelerySettings:
    task_track_started = True
    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]
    enable_utc = True
    worker_prefetch_multiplier = 1
    # --- FORCES THE COMPLETE DEACTIVATION OF THE TEMPORARY QUEUE COMPONENT ---
    worker_enable_remote_control = False


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


@cache
def get_http_server_settings() -> HTTPServerSettings:
    return HTTPServerSettings()


@cache
def get_redis_settings() -> RedisSettings:
    return RedisSettings()


@cache
def get_rabbitmq_settings() -> RabbitMQSettings:
    return RabbitMQSettings()


@cache
def get_mongodb_settings() -> MongoDBSettings:
    return MongoDBSettings()
