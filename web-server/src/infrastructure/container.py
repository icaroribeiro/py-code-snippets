from dependency_injector import containers, providers
from pymongo import AsyncMongoClient

from adapters.outbound.health.service import Service
from adapters.outbound.messaging.redis.publishers.event_publisher import EventPublisher
from adapters.outbound.persistence.mongodb.repositories.task_repository import (
    TaskRepository,
)
from adapters.outbound.task_queue.task_manager import TaskManager
from core.use_cases.health_use_case import HealthUseCase
from core.use_cases.task_use_case import TaskUseCase
from infrastructure.celery.broker import CeleryBroker
from infrastructure.config import (
    MongoDBSettings,
    RabbitMQSettings,
    RedisSettings,
    get_mongodb_settings,
    get_rabbitmq_settings,
    get_redis_settings,
)
from infrastructure.mongodb.database import MongoDBDatabase
from infrastructure.mongodb.migration_manager import MigrationManager
from infrastructure.redis.database import RedisDatabase


async def init_redis_database_resource(redis_config: RedisSettings):
    redis_wrapper = RedisDatabase(url=redis_config.rate_limit_url)
    await redis_wrapper.init()
    yield redis_wrapper
    await redis_wrapper.shutdown()


def init_celery_broker_resource(
    rabbitmq_config: RabbitMQSettings, redis_config: RedisSettings
):
    celery_broker_wrapper = CeleryBroker(
        broker_url=rabbitmq_config.url, backend_url=redis_config.backend_url
    )
    celery_broker_wrapper.init()
    yield celery_broker_wrapper


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
    wiring_config = containers.WiringConfiguration(
        packages=["src.infrastructure.celery.tasks"]
    )

    redis_config = providers.Singleton(get_redis_settings)

    rabbitmq_config = providers.Singleton(get_rabbitmq_settings)

    mongodb_config = providers.Singleton(get_mongodb_settings)

    redis_database = providers.Resource(
        init_redis_database_resource,
        redis_config=redis_config,
    )

    celery_broker = providers.Resource(
        init_celery_broker_resource,
        rabbitmq_config=rabbitmq_config,
        redis_config=redis_config,
    )

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
        Service,
        mongodb_database=mongodb_database,
        redis_database=redis_database,
        celery_broker=celery_broker,
    )

    health_use_case = providers.Factory(
        HealthUseCase,
        service=health_service,
    )

    task_repository = providers.Factory(TaskRepository)

    event_publisher = providers.Singleton(
        EventPublisher,
        redis_url=redis_config.provided.rate_limit_url,
    )

    task_manager = providers.Factory(TaskManager)

    task_use_case = providers.Factory(
        TaskUseCase,
        repository=task_repository,
        publisher=event_publisher,
        manager=task_manager,
    )
