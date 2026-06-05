from beanie import init_beanie
from pymongo import AsyncMongoClient

from core.logging.logger_factory import get_logger
from src.adapters.out.mongodb.documents.i18n_document import I18nDocument
from src.infrastructure.mongodb.migration_manager import MigrationManager

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
        self.db = None

    async def init(self):
        self.db = self._client[self._database_name]
        await self._migration_manager.run_migrations()
        await init_beanie(database=self.db, document_models=[I18nDocument])
        logger.info(
            f"Beanie initialized with MongoDB successfully and {len(I18nDocument.Settings.name)} documents."
        )
        return self.db

    async def shutdown(self):
        await self._client.close()
