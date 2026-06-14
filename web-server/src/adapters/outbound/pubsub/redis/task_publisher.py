import json
from typing import Any

from core.ports.outbound.task_port import (
    TaskPublisherOutputPort,
)
from infrastructure.cross_cutting.logging import get_logger
from infrastructure.redis.storage import RedisStorage

logger = get_logger(__name__)


class RedisTaskPublisher(TaskPublisherOutputPort):
    def __init__(self, redis_storage: RedisStorage) -> None:
        self._redis_storage = redis_storage

    async def publish(self, channel: str, message: dict[str, Any]) -> None:
        try:
            if self._redis_storage.client is not None:
                payload = json.dumps(message)
                await self._redis_storage.client.publish(channel, payload)
                logger.info(f"Event successfully streamed to Redis channel: {channel}")
        except Exception as error:
            logger.error(f"Failed to publish message to channel {channel}: {error}")
