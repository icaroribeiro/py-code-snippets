from beanie import free_fall_migration
from pymongo.asynchronous.client_session import AsyncClientSession

from src.adapters.out.mongodb.documents.i18n_document import I18nDocument
from src.core.logging.logger_factory import get_logger

logger = get_logger(__name__)


class Forward:
    @free_fall_migration(document_models=[I18nDocument])
    async def upgrade(self, session: AsyncClientSession | None = None):
        """
        Seeds initial translation dictionary data using high-level Beanie Document APIs.
        """
        logger.info("Starting seeding initial translations...")

        seeds = [
            I18nDocument(
                locale_key="en-US:welcome_msg",
                lang="en-US",
                key="welcome_msg",
                text="Hello! Welcome to our health assistant bot.",
            ),
            I18nDocument(
                locale_key="pt-BR:welcome_msg",
                lang="pt-BR",
                key="welcome_msg",
                text="Olá! Bem-vindo ao nosso bot de assistência à saúde.",
            ),
            I18nDocument(
                locale_key="en-US:error_generic",
                lang="en-US",
                key="error_generic",
                text="An unexpected error occurred. Please try again later.",
            ),
            I18nDocument(
                locale_key="pt-BR:error_generic",
                lang="pt-BR",
                key="error_generic",
                text="Ocorreu um erro inesperado. Por favor, tente novamente mais tarde.",
            ),
        ]

        try:
            # Executes upsert logic sequentially ensuring transaction safety
            for seed in seeds:
                # 1. Try to find the existing record using the transaction session
                existing_doc = await I18nDocument.find_one(
                    I18nDocument.locale_key == seed.locale_key, session=session
                )

                if existing_doc:
                    # 2. If it exists, update the necessary fields while keeping the ID intact
                    existing_doc.text = seed.text
                    await existing_doc.save(session=session)
                else:
                    # 3. If it's new, insert from scratch
                    await seed.insert(session=session)
            logger.info("Initial translations seeded successfully.")
        except Exception as error:
            logger.error(f"Failed to complete structural data seeding: {repr(error)}")
            raise error


class Backward:
    @free_fall_migration(document_models=[I18nDocument])
    async def downgrade(self, session: AsyncClientSession | None = None):
        """
        Cleanses seeded key mutations from the translation table inside the migration session.
        """
        logger.info("Starting removing seeded translations...")
        seeded_keys = ["welcome_msg", "error_generic"]

        try:
            # Utilizes Beanie find and delete clauses contextually bound to the session
            await I18nDocument.find(
                {"key": {"$in": seeded_keys}}, session=session
            ).delete()
            logger.info("Seeded translations removed successfully.")
        except Exception as error:
            logger.error(f"Failed to reverse translation data seeding: {repr(error)}")
            raise error
