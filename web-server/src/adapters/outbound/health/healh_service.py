import asyncio
from typing import Any, Dict

from src.core.domain.health import HealthStatus
from src.core.logging.logger_factory import get_logger
from src.infrastructure.celery.message_broker import CeleryMessageBroker
from src.infrastructure.mongodb.database import MongoDBDatabase
from src.infrastructure.redis import RedisDatabase
from src.ports.outbound.health.health_service import HealthServicePort

logger = get_logger(__name__)


class HealthService(HealthServicePort):
    def __init__(
        self,
        mongodb_database: MongoDBDatabase,
        redis_database: RedisDatabase,
        celery_message_broker: CeleryMessageBroker,
    ) -> None:
        self._mongodb_database = mongodb_database
        self._redis_database = redis_database
        self._celery_message_broker = celery_message_broker

    async def check_services_availability(self) -> Dict[str, str]:
        results = await asyncio.gather(
            self._check_mongodb_database(),
            self._check_redis_database(),
            self._check_celery_message_broker(),
            return_exceptions=False,
        )

        return {
            "mongodb": results[0],
            "redis": results[1],
            "celery_and_rabbitmq": results[2],
        }

    async def _check_mongodb_database(self) -> str:
        try:
            if self._mongodb_database.client is not None:
                await self._mongodb_database.client.admin.command("ping")
                return HealthStatus.HEALTHY
        except Exception as error:
            logger.error(f"MongoDB connection health check failed: {error}")
        return HealthStatus.UNHEALTHY

    async def _check_redis_database(self) -> str:
        try:
            if self._redis_database.client is not None:
                await self._redis_database.client.ping()
                return HealthStatus.HEALTHY
        except Exception as error:
            logger.error(f"Redis connection health check failed: {error}")
        return HealthStatus.UNHEALTHY

    async def _check_celery_message_broker(self) -> str:
        try:
            if not self._celery_message_broker:
                logger.error("Celery message broker component is missing")
                return HealthStatus.UNHEALTHY

            celery_app: Any = self._celery_message_broker.app
            if celery_app is None:
                logger.error("Celery app instance is uninitialized (None)")
                return HealthStatus.UNHEALTHY

            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, lambda: celery_app.control.ping())

            return HealthStatus.HEALTHY
        except Exception as error:
            logger.error(f"Celery/RabbitMQ connection health check failed: {error}")
        return HealthStatus.UNHEALTHY
