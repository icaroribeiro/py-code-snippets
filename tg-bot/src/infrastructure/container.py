from dependency_injector import containers, providers
from pymongo import AsyncMongoClient

from adapters.outbound.system.health.checker import HealthChecker
from core.use_cases.health_use_case import HealthCheckUseCase, HealthUseCase
from core.use_cases.telegram_use_case import TelegramUseCase
from infrastructure.config import (
    MongoDBSettings,
    get_mongodb_settings,
)
from infrastructure.mongodb.database import MongoDBDatabase
from infrastructure.mongodb.migration_manager import MigrationManager


async def init_mongodb_database_resource(
    mongodb_config: MongoDBSettings,
    mongo_client: AsyncMongoClient,
    migration_manager: MigrationManager,
):
    database_wrapper = MongoDBDatabase(
        client=mongo_client,
        database_name=mongodb_config.database,
        migration_manager=migration_manager,
    )
    await database_wrapper.init()
    yield database_wrapper
    await database_wrapper.shutdown()


class Container(containers.DeclarativeContainer):
    mongodb_config = providers.Singleton(get_mongodb_settings)

    mongo_client = providers.Singleton(AsyncMongoClient, mongodb_config.provided.uri)
    migration_manager = providers.Factory(
        MigrationManager,
        database_uri=mongodb_config.provided.uri,
        database_name=mongodb_config.provided.database,
        migrations_path=mongodb_config.provided.migrations_path,
    )

    mongodb_database = providers.Resource(
        init_mongodb_database_resource,
        mongodb_config=mongodb_config,
        mongo_client=mongo_client,
        migration_manager=migration_manager,
    )

    health_checker_adapter = providers.Factory(
        HealthChecker,
        mongodb_database=mongodb_database,
    )

    health_check_use_case = providers.Factory(
        HealthCheckUseCase,
        health_checker=health_checker_adapter,
    )

    telegram_use_case = providers.Factory(TelegramUseCase)
