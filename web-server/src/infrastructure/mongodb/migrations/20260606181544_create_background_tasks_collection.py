from beanie import free_fall_migration
from pymongo.asynchronous.client_session import AsyncClientSession

from adapters.outbound.persistence.documents.task_document import (
    TaskDocument,
)
from infrastructure.logging import get_logger

logger = get_logger(__name__)


class Forward:
    @free_fall_migration(document_models=[TaskDocument])
    async def upgrade(self, session: AsyncClientSession | None = None) -> None:
        """
        The tasks collection and its indexed fields are implicitly
        provisioned by Beanie initialization before this block executes.
        """
        logger.info("Collection 'tasks' initialization verified by Beanie.")


class Backward:
    @free_fall_migration(document_models=[TaskDocument])
    async def downgrade(self, session: AsyncClientSession | None = None) -> None:
        """
        Drops the core tasks database structures during complete stack teardowns.
        """
        logger.info("Starting dropping collection 'tasks'...")
        async_collection = TaskDocument.get_pymongo_collection()
        await async_collection.database.drop_collection(
            name_or_collection=TaskDocument.Settings.name,
            session=session,
        )
        logger.info("Collection 'tasks' dropped successfully.")
