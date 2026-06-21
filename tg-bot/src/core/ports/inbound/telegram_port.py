from abc import ABC, abstractmethod
from typing import Any

from core.domain import TaskResult


class TelegramWebhookInputPort(ABC):
    @abstractmethod
    async def process_update(self, raw_update: dict[str, Any]) -> None:
        """Processes an incoming raw Update payload directly from Telegram's Webhook network boundary."""
        pass


class TelegramTaskCallbackInputPort(ABC):
    @abstractmethod
    async def process_result(self, task_result: TaskResult) -> None:
        """Executes the business logic for a completed background task."""
        pass
