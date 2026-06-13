import asyncio
from typing import Dict

from core.domain.health import HealthStatus
from core.ports.outbound.health_port import HealthCheckerOutputPort
from infrastructure.celery.broker import CeleryBroker
from infrastructure.cross_cutting.logging import get_logger
from infrastructure.mongodb.database import MongoDBDatabase
from infrastructure.redis.storage import RedisStorage

logger = get_logger(__name__)


class HealthChecker(HealthCheckerOutputPort):
    def __init__(
        self,
        mongodb_database: MongoDBDatabase,
        redis_storage: RedisStorage,
        celery_broker: CeleryBroker,
    ) -> None:
        self._mongodb_database = mongodb_database
        self._redis_storage = redis_storage
        self._celery_broker = celery_broker

    async def check_services_availability(self) -> Dict[str, str]:
        results = await asyncio.gather(
            self._check_mongodb_database(),
            self._check_redis_storage(),
            self._check_celery_broker(),
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

    async def _check_redis_storage(self) -> str:
        try:
            if self._redis_storage.client is not None:
                await self._redis_storage.client.ping()
                return HealthStatus.HEALTHY
        except Exception as error:
            logger.error(f"Redis connection health check failed: {error}")
        return HealthStatus.UNHEALTHY

    async def _check_celery_broker(self) -> str:
        try:
            if not self._celery_broker:
                logger.error("Celery message broker component is missing")
                return HealthStatus.UNHEALTHY

            celery_app = self._celery_broker.app
            if celery_app is None:
                logger.error("Celery app instance is uninitialized (None)")
                return HealthStatus.UNHEALTHY

            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None, lambda: celery_app.connection_for_write().connect()
            )

            return HealthStatus.HEALTHY
        except Exception as error:
            logger.error(f"Celery/RabbitMQ connection health check failed: {error}")
        return HealthStatus.UNHEALTHY
