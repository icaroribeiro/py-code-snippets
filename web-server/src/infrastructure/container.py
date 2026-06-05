from dependency_injector import containers, providers
from pymongo import AsyncMongoClient

from adapters.outbound.health.healh_service import HealthService
from core.usecase.check_health_usecase import CheckHealthUseCase
from infrastructure.celery.message_broker import CeleryMessageBroker
from infrastructure.redis import RedisDatabase
from src.infrastructure.config import (
    MongoDBSettings,
    RabbitMQSettings,
    RedisSettings,
    get_mongodb_settings,
    get_rabbitmq_settings,
    get_redis_settings,
)
from src.infrastructure.mongodb.database import MongoDBDatabase
from src.infrastructure.mongodb.migration_manager import MigrationManager


async def init_redis_database_resource(redis_config: RedisSettings):
    redis_wrapper = RedisDatabase(url=redis_config.rate_limit_url)
    await redis_wrapper.init()
    yield redis_wrapper
    await redis_wrapper.shutdown()


def init_celery_message_broker_resource(
    rabbitmq_config: RabbitMQSettings, redis_config: RedisSettings
):
    celery_message_broker_wrapper = CeleryMessageBroker(
        broker_url=rabbitmq_config.url, backend_url=redis_config.backend_url
    )
    yield celery_message_broker_wrapper.init()


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
    redis_config = providers.Singleton(get_redis_settings)

    redis_database = providers.Resource(
        init_redis_database_resource,
        redis_config=redis_config,
    )

    rabbitmq_config = providers.Singleton(get_rabbitmq_settings)

    celery_message_broker = providers.Resource(
        init_celery_message_broker_resource,
        rabbitmq_config=rabbitmq_config,
        redis_config=redis_config,
    )

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

    health_service = providers.Factory(
        HealthService,
        mongodb_database=mongodb_database,
        redis_database=redis_database,
        celery_message_broker=celery_message_broker,
    )

    check_health_usecase = providers.Factory(
        CheckHealthUseCase,
        health_service=health_service,
    )
