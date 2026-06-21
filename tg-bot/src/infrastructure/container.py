from aiogram import Bot, Dispatcher
from dependency_injector import containers, providers
from pymongo import AsyncMongoClient

from adapters.inbound.telegram.dispatcher import TelegramDispatcher
from adapters.inbound.telegram.menus.bot_menu import TelegramBotMenu
from adapters.outbound.external_apis.task_service_api import TaskServiceApi
from adapters.outbound.system.health_check import HealthCheck
from core.use_cases.health_use_case import HealthCheckUseCase
from core.use_cases.telegram_use_case import (
    TelegramTaskCallbackUseCase,
    TelegramWebhookUseCase,
)
from infrastructure.config import (
    MongoDBSettings,
    get_http_client_settings,
    get_mongodb_settings,
    get_task_service_api_settings,
    get_telegram_settings,
)
from infrastructure.http_client import HTTPClient
from infrastructure.i18n.localization_service import LocalizationService
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
    bot_menu: TelegramBotMenu, localization_service: LocalizationService
) -> Dispatcher:
    dispatcher_wrapper = TelegramDispatcher(
        bot_menu=bot_menu, localization_service=localization_service
    )
    return dispatcher_wrapper.init()


class Container(containers.DeclarativeContainer):
    http_client_settings = providers.Singleton(get_http_client_settings)

    mongodb_settings = providers.Singleton(get_mongodb_settings)

    task_service_api_settings = providers.Singleton(get_task_service_api_settings)

    telegram_settings = providers.Singleton(get_telegram_settings)

    bot = providers.Singleton(
        Bot,
        token=telegram_settings.provided.bot_token,
    )

    localization_service = providers.Singleton(
        LocalizationService, default_lang="en-US"
    )

    telegram_bot_menu = providers.Singleton(TelegramBotMenu, localization_service)

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

    task_service_api_adapter = providers.Singleton(
        TaskServiceApi,
        http_client=http_client,
        settings=task_service_api_settings,
    )

    health_check_use_case = providers.Factory(
        HealthCheckUseCase,
        health_checker=health_checker_adapter,
    )

    telegram_dispatcher = providers.Singleton(
        init_telegram_dispatcher,
        bot_menu=telegram_bot_menu,
        localization_service=localization_service,
    )

    telegram_webhook_use_case = providers.Factory(
        TelegramWebhookUseCase, bot=bot, dispatcher=telegram_dispatcher
    )

    telegram_task_callback_use_case = providers.Singleton(
        TelegramTaskCallbackUseCase, bot=bot, localization_service=localization_service
    )
