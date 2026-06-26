from aiogram import Bot, Dispatcher
from dependency_injector import containers, providers
from pymongo import AsyncMongoClient

from adapters.outbound.external_apis import TaskServiceApi
from adapters.outbound.system import HealthCheck
from core.use_cases import (
    BotTaskCallbackUseCase,
    BotWebhookUseCase,
    HealthCheckUseCase,
)
from infrastructure.config import (
    MongoDBSettings,
    get_http_client_settings,
    get_mongodb_settings,
    get_task_service_api_settings,
    get_telegram_settings,
)
from infrastructure.http_client import HTTPClient
from infrastructure.i18n import i18nService
from infrastructure.mongodb import MigrationManager, MongoDBDatabase
from telegram import TelegramDispatcher, TelegramMenu


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
    menu: TelegramMenu, i18n_service: i18nService
) -> Dispatcher:
    dispatcher_wrapper = TelegramDispatcher(menu=menu, i18n_service=i18n_service)
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

    i18n_service = providers.Singleton(i18nService, default_lang="en-US")

    telegram_bot_menu = providers.Singleton(
        TelegramMenu, telegram_settings, i18n_service
    )

    mongo_client = providers.Singleton(AsyncMongoClient, mongodb_settings.provided.uri)
    migration_manager = providers.Factory(
        MigrationManager,
        mongodb_settings.provided.uri,
        mongodb_settings.provided.database,
        mongodb_settings.provided.migrations_path,
    )

    mongodb_database = providers.Resource(
        init_mongodb_database_resource,
        mongodb_settings,
        mongo_client,
        migration_manager,
    )

    health_checker_adapter = providers.Factory(
        HealthCheck,
        mongodb_database,
    )

    http_client = providers.Factory(HTTPClient, http_client_settings)

    task_service_api_adapter = providers.Singleton(
        TaskServiceApi,
        http_client,
        task_service_api_settings,
    )

    health_check_use_case = providers.Factory(
        HealthCheckUseCase,
        health_checker_adapter,
    )

    telegram_dispatcher = providers.Singleton(
        init_telegram_dispatcher,
        telegram_bot_menu,
        i18n_service,
    )

    bot_webhook_use_case = providers.Factory(
        BotWebhookUseCase, bot, telegram_dispatcher
    )

    bot_task_callback_use_case = providers.Singleton(
        BotTaskCallbackUseCase, bot, i18n_service
    )
