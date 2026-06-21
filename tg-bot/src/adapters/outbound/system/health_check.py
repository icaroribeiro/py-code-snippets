import asyncio
from typing import Dict

from core.domain.health import HealthStatus
from core.ports.outbound.health_port import HealthCheckOutputPort
from infrastructure.cross_cutting.logging import get_logger
from infrastructure.mongodb.database import MongoDBDatabase

logger = get_logger(__name__)


class HealthCheck(HealthCheckOutputPort):
    def __init__(
        self,
        mongodb_database: MongoDBDatabase,
    ) -> None:
        self._mongodb_database = mongodb_database

    async def check_services_availability(self) -> Dict[str, str]:
        results = await asyncio.gather(
            self._check_mongodb_database(),
            return_exceptions=False,
        )

        return {"mongodb": results[0]}

    async def _check_mongodb_database(self) -> str:
        try:
            if self._mongodb_database.client is not None:
                await self._mongodb_database.client.admin.command("ping")
                return HealthStatus.HEALTHY
        except Exception as error:
            logger.error(f"MongoDB connection health check failed: {error}")
        return HealthStatus.UNHEALTHY
