from abc import ABC, abstractmethod
from typing import Any

class TelegramInputPort(ABC):
    @abstractmethod
    async def process_update(self, raw_update: dict[str, Any]) -> None:
        """Processes an incoming raw Update payload directly from Telegram's Webhook network boundary."""
        pass
