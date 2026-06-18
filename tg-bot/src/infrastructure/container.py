from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from dependency_injector import containers, providers
from pymongo import AsyncMongoClient

from adapters.inbound.telegram.commands.bot_commands import BotCommands
from adapters.inbound.telegram.handlers.hello_world_handler import (
    router as hello_world_router,
)
from adapters.outbound.external_apis.clients.task_service_client import (
    TaskServiceClient,
)
from adapters.outbound.system.health.checker import HealthChecker
from core.use_cases.health_use_case import HealthCheckUseCase
from core.use_cases.hello_world_use_case import HelloWorldUseCase
from core.use_cases.task_callback_use_case import TaskCallbackUseCase
from core.use_cases.telegram_use_case import TelegramUseCase
from infrastructure.config import (
    MongoDBSettings,
    get_http_client_settings,
    get_mongodb_settings,
    get_task_service_settings,
    get_telegram_settings,
)
from infrastructure.cross_cutting.i18n_service import I18nService
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


def init_telegram_dispatcher(
    bot: Bot, i18n_service: I18nService, hello_world_use_case: HelloWorldUseCase
) -> Dispatcher:
    dp = Dispatcher()
    bot_commands = BotCommands(i18n_service=i18n_service)
    dp.startup.register(bot_commands.register_all)
    dp["hello_world_use_case"] = hello_world_use_case
    dp.include_router(hello_world_router)
    setup_dialogs(dp)
    return dp


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

    health_check_use_case = providers.Factory(
        HealthCheckUseCase,
        health_checker=health_checker_adapter,
    )

    i18n_service = providers.Singleton(I18nService, default_lang="en-US")

    bot = providers.Singleton(
        Bot,
        token=telegram_settings.provided.bot_token,
    )

    heelo_worold_use_case = providers.Factory(
        HelloWorldUseCase,
        bot=bot,
    )

    telegram_dispatcher = providers.Singleton(
        init_telegram_dispatcher,
        bot=bot,
        i18n_service=i18n_service,
        hello_world_use_case=heelo_worold_use_case,
    )

    telegram_use_case = providers.Factory(
        TelegramUseCase,
        bot=bot,
        dispatcher=telegram_dispatcher,
        task_service=task_service_client_adapter,
    )

    task_callback_use_case = providers.Singleton(
        TaskCallbackUseCase, bot=bot, i18n=i18n_service
    )
