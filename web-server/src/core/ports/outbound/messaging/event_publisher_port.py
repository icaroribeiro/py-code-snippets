from abc import ABC, abstractmethod
from typing import Any


class EventPublisherPort(ABC):
    @abstractmethod
    async def publish(self, channel: str, message: dict[str, Any]) -> None:
        pass
