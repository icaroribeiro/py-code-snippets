from beanie import free_fall_migration
from pymongo.asynchronous.client_session import AsyncClientSession

from src.adapters.out.mongodb.documents.i18n_document import I18nDocument
from src.core.logging.logger_factory import get_logger

logger = get_logger(__name__)


class Forward:
    @free_fall_migration(document_models=[I18nDocument])
    async def upgrade(self, session: AsyncClientSession | None = None):
        """
        The i18n collection and its dynamic single/compound indexes are
        implicitly provisioned by Beanie initialization before this block executes.
        """
        logger.info("Collection 'i18n_dictionary' initialization verified by Beanie.")


class Backward:
    @free_fall_migration(document_models=[I18nDocument])
    async def downgrade(self, session: AsyncClientSession | None = None):
        """
        Drops the core i18n database structures during complete stack teardowns.
        """
        logger.info("Starting dropping collection 'i18n_dictionary'...")
        async_collection = I18nDocument.get_pymongo_collection()
        await async_collection.database.drop_collection(
            name_or_collection=I18nDocument.Settings.name, session=session
        )
        logger.info("Collection 'i18n_dictionary' dropped successfully.")
