from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from dependency_injector import containers, providers
from pymongo import AsyncMongoClient

from adapters.outbound.external_apis.clients.task_service_client import (
    TaskServiceClient,
)
from adapters.outbound.system.health.checker import HealthChecker
from core.use_cases.health_use_case import HealthCheckUseCase
from core.use_cases.telegram_use_case import TelegramUseCase
from infrastructure.config import (
    MongoDBSettings,
    get_http_client_settings,
    get_mongodb_settings,
    get_task_service_settings,
    get_telegram_settings,
)
from infrastructure.http_client import HTTPClient
from infrastructure.mongodb.database import MongoDBDatabase
from infrastructure.mongodb.migration_manager import MigrationManager


async def init_mongodb_database_resource(
    mongodb_settings: MongoDBSettings,
    mongo_client: AsyncMongoClient,
    migration_manager: MigrationManager,
):
    database_wrapper = MongoDBDatabase(
        client=mongo_client,
        database_name=mongodb_settings.database,
        migration_manager=migration_manager,
    )
    await database_wrapper.init()
    yield database_wrapper
    await database_wrapper.shutdown()


class Container(containers.DeclarativeContainer):
    http_client_settings = providers.Singleton(get_http_client_settings)

    telegram_settings = providers.Singleton(get_telegram_settings)

    task_service_settings = providers.Singleton(get_task_service_settings)

    mongodb_settings = providers.Singleton(get_mongodb_settings)

    mongo_client = providers.Singleton(AsyncMongoClient, mongodb_settings.provided.uri)
    migration_manager = providers.Factory(
        MigrationManager,
        database_uri=mongodb_settings.provided.uri,
        database_name=mongodb_settings.provided.database,
        migrations_path=mongodb_settings.provided.migrations_path,
    )

    mongodb_database = providers.Resource(
        init_mongodb_database_resource,
        mongodb_settings=mongodb_settings,
        mongo_client=mongo_client,
        migration_manager=migration_manager,
    )

    health_checker_adapter = providers.Factory(
        HealthChecker,
        mongodb_database=mongodb_database,
    )

    http_client = providers.Factory(HTTPClient, settings=http_client_settings)

    task_service_client_adapter = providers.Singleton(
        TaskServiceClient,
        http_client=http_client,
        settings=task_service_settings,
    )

    telegram_bot = providers.Singleton(
        Bot,
        token=telegram_settings.provided.bot_token,
    )

    @providers.Singleton
    def telegram_dispatcher() -> Dispatcher:
        dp = Dispatcher()
        # ----------------------------------------------------------------------
        # Here you will register your dialog routers (aiogram-dialog)
        # Example:
        # from ui.telegram.dialogs import main_dialog
        # dp.include_router(main_dialog)
        # ----------------------------------------------------------------------
        # Activates the aiogram-dialog engine natively in the dispatcher pipeline
        setup_dialogs(dp)
        return dp

    health_check_use_case = providers.Factory(
        HealthCheckUseCase,
        health_checker=health_checker_adapter,
    )

    telegram_use_case = providers.Factory(
        TelegramUseCase,
        bot=telegram_bot,
        dispatcher=telegram_dispatcher,
        task_service=task_service_client_adapter,
    )
