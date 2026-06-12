from dependency_injector import containers, providers
from pymongo import AsyncMongoClient

from adapters.outbound.health.checker import HealthChecker
from adapters.outbound.task.persistence.repository import (
    TaskRepository,
)
from adapters.outbound.task.task_queue.event_publisher import TaskEventPublisher
from adapters.outbound.task.task_queue.orchestrator import TaskOrchestrator
from core.use_cases.health.use_case import HealthUseCase
from core.use_cases.task.use_case import TaskUseCase
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
from infrastructure.redis.storage import RedisStorage


async def init_redis_storage_resource(redis_config: RedisSettings):
    redis_wrapper = RedisStorage(url=redis_config.backend_url)
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
    redis_config = providers.Singleton(get_redis_settings)

    rabbitmq_config = providers.Singleton(get_rabbitmq_settings)

    mongodb_config = providers.Singleton(get_mongodb_settings)

    redis_storage = providers.Resource(
        init_redis_storage_resource,
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

    health_checker = providers.Factory(
        HealthChecker,
        mongodb_database=mongodb_database,
        redis_storage=redis_storage,
        celery_broker=celery_broker,
    )

    health_use_case = providers.Factory(
        HealthUseCase,
        health_checker=health_checker,
    )

    task_orchestrator = providers.Factory(
        TaskOrchestrator,
    )

    task_repository = providers.Factory(TaskRepository)

    task_event_publisher = providers.Singleton(
        TaskEventPublisher,
        redis_storage=redis_storage,
    )

    task_use_case = providers.Factory(
        TaskUseCase,
        task_repository=task_repository,
        task_orchestrator=task_orchestrator,
        task_event_publisher=task_event_publisher,
    )
