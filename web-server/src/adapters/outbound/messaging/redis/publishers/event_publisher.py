import json
from typing import Any

import redis.asyncio as aioredis

from core.ports.outbound.messaging.event_publisher_port import EventPublisherPort
from infrastructure.logging import get_logger

logger = get_logger(__name__)


class EventPublisher(EventPublisherPort):
    def __init__(self, redis_url: str) -> None:
        self._redis = aioredis.from_url(redis_url, decode_responses=True)

    async def publish(self, channel: str, message: dict[str, Any]) -> None:
        try:
            payload = json.dumps(message)
            await self._redis.publish(channel, payload)
            logger.info(f"Event successfully streamed to Redis channel: {channel}")
        except Exception as error:
            logger.error(f"Failed to publish message to channel {channel}: {error}")
