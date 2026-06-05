from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from core.usecase.check_health_usecase import CheckHealthUseCase
from src.infrastructure.celery.message_broker import CeleryMessageBroker
from src.infrastructure.container import Container
from src.infrastructure.mongodb.database import MongoDBDatabase
from src.infrastructure.redis.database import RedisDatabase


class Dependencies:
    @staticmethod
    @inject
    def redis_database(
        instance: Annotated[RedisDatabase, Depends(Provide[Container.redis])],
    ) -> RedisDatabase:
        return instance

    @staticmethod
    @inject
    def celery_message_broker(
        celery_message_broker: Annotated[
            CeleryMessageBroker, Depends(Provide[Container.celery_message_broker])
        ],
    ) -> CeleryMessageBroker:
        return celery_message_broker

    @staticmethod
    @inject
    def mongodb_database(
        mongodb_database: Annotated[
            MongoDBDatabase, Depends(Provide[Container.mongodb_database])
        ],
    ) -> MongoDBDatabase:
        return mongodb_database

    @staticmethod
    @inject
    def check_health_usecase(
        check_health_usecase: Annotated[
            CheckHealthUseCase, Depends(Provide[Container.check_health_usecase])
        ],
    ) -> CheckHealthUseCase:
        return check_health_usecase
