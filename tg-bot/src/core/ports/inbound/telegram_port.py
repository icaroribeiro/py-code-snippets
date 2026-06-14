from abc import ABC, abstractmethod
from typing import Any

from aiogram import Bot, Dispatcher


class TelegramInputPort(ABC):
    @abstractmethod
    async def foo(
        self, json_data: dict[str, Any], bot: Bot | None, dispatcher: Dispatcher | None
    ) -> None:
        pass
