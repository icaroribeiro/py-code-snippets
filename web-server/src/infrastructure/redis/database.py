import redis.asyncio as aioredis

from infrastructure.logging import get_logger

logger = get_logger(__name__)


class RedisDatabase:
    def __init__(self, url: str) -> None:
        self._url = url
        self.client: aioredis.Redis | None = None

    async def init(self) -> aioredis.Redis:
        logger.info("Initializing Redis connection pool...")
        self.client = aioredis.from_url(
            self._url, encoding="utf-8", decode_responses=True
        )
        if self.client is None:
            raise RuntimeError("Failed to initialize Redis connection")
        return self.client

    async def shutdown(self):
        if self.client is None:
            raise RuntimeError("Failed to close Redis connection")
        logger.info("Closing Redis connection pool...")
        await self.client.close()
        logger.info("Redis pool closed successfully.")
