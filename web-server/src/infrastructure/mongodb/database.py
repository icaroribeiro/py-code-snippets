from beanie import init_beanie
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from adapters.outbound.task.persistence.documents import (
    TaskDocument,
)
from infrastructure.cross_cutting.logging import get_logger
from infrastructure.mongodb.migration_manager import MigrationManager

logger = get_logger(__name__)


class MongoDBDatabase:
    def __init__(
        self,
        client: AsyncMongoClient,
        database_name: str,
        migration_manager: MigrationManager,
    ) -> None:
        self._client = client
        self._database_name = database_name
        self._migration_manager = migration_manager
        self.db: AsyncDatabase | None = None

    @property
    def client(self) -> AsyncMongoClient:
        """Exposes the internal client safely for health checks and extensions."""
        return self._client

    async def init(self) -> AsyncDatabase:
        self.db = self._client[self._database_name]
        await self._migration_manager.run_migrations()
        logger.info(f"Initializing Beanie ODM with database: {self._database_name}")
        await init_beanie(database=self.db, document_models=[TaskDocument])
        if self.db is None:
            raise RuntimeError("Failed to initialize MongoDB connection")
        return self.db

    async def shutdown(self):
        if self.db is None:
            raise RuntimeError("Failed to close MongoDB connection")
        logger.info("Closing MongoDB connection...")
        await self._client.close()
        logger.info("MongoDB connection closed successfully.")
