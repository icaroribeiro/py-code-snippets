from dependency_injector import containers, providers
from pymongo import AsyncMongoClient

from src.adapters.out.mongodb.repositories.i18n_repository import I18nRepository
from src.core.usecase.get_i18n_text_usecase import GetI18nTextUseCase
from src.infrastructure.config import get_i18n_settings, get_mongodb_settings
from src.infrastructure.mongodb.database import MongoDBDatabase
from src.infrastructure.mongodb.migration_manager import MigrationManager


async def init_mongodb_resource(mongodb_config, mongo_client, migration_manager):
    """
    Asynchronous initializer function for the MongoDBDatabase resource.
    Ensures that the init() method is awaited before the application starts consuming dependencies.
    """
    database_wrapper = MongoDBDatabase(
        client=mongo_client,
        database_name=mongodb_config.database,
        migration_manager=migration_manager,
    )

    # Executes the init() method that you discovered was being ignored
    await database_wrapper.init()

    yield database_wrapper

    # Executes the shutdown() method to ensure proper cleanup of the connection pool when the app closes
    await database_wrapper.shutdown()


class Container(containers.DeclarativeContainer):
    i18n_config = providers.Singleton(get_i18n_settings)

    mongodb_config = providers.Singleton(get_mongodb_settings)

    mongo_client = providers.Singleton(AsyncMongoClient, mongodb_config.provided.uri)

    migration_manager = providers.Factory(
        MigrationManager,
        database_uri=mongodb_config.provided.uri,
        database_name=mongodb_config.provided.database,
        migrations_path=mongodb_config.provided.migrations_path,
    )

    mongodb = providers.Resource(
        init_mongodb_resource,
        mongodb_config=mongodb_config,
        mongo_client=mongo_client,
        migration_manager=migration_manager,
    )

    i18n_repository = providers.Factory(
        I18nRepository, config=i18n_config, database_wrapper=mongodb.provided
    )

    get_i18n_text_usecase = providers.Factory(
        GetI18nTextUseCase, i18n_repository=i18n_repository
    )
