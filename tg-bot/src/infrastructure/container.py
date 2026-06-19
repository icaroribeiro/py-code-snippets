from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from dependency_injector import containers, providers
from pymongo import AsyncMongoClient

from adapters.outbound.external_apis.clients.task_service_client import (
    TaskServiceClient,
)
from adapters.outbound.system.health.checker import HealthCheck
from core.use_cases.health_use_case import HealthCheckUseCase
from core.use_cases.hello_world_use_case import HelloWorldUseCase
from core.use_cases.task_callback_use_case import TaskCallbackUseCase
from core.use_cases.tg_feed_update_use_case import TgFeedUpdateUseCase
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
from infrastructure.telegram.menu.bot_menu import TgBotMenu


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
    tg_bot_commands: TgBotMenu, hello_world_use_case: HelloWorldUseCase
) -> Dispatcher:
    dp = Dispatcher()
    dp.startup.register(tg_bot_commands.register_all)
    # dp["hello_world_use_case"] = hello_world_use_case
    # dp.include_router(hello_world_router)
    setup_dialogs(dp)
    return dp


class Container(containers.DeclarativeContainer):
    http_client_settings = providers.Singleton(get_http_client_settings)

    telegram_settings = providers.Singleton(get_telegram_settings)

    task_service_settings = providers.Singleton(get_task_service_settings)

    mongodb_settings = providers.Singleton(get_mongodb_settings)

    bot = providers.Singleton(
        Bot,
        token=telegram_settings.provided.bot_token,
    )

    i18n_service = providers.Singleton(I18nService, default_lang="en-US")

    tg_bot_commands = providers.Singleton(TgBotMenu, i18n_service)

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
        HealthCheck,
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

    heelo_worold_use_case = providers.Factory(
        HelloWorldUseCase,
        bot=bot,
    )

    telegram_dispatcher = providers.Singleton(
        init_telegram_dispatcher,
        tg_bot_commands=tg_bot_commands,
        hello_world_use_case=heelo_worold_use_case,
    )

    tg_feed_update_use_case = providers.Factory(
        TgFeedUpdateUseCase, bot=bot, dispatcher=telegram_dispatcher
    )

    task_callback_use_case = providers.Singleton(
        TaskCallbackUseCase, bot=bot, i18n=i18n_service
    )
