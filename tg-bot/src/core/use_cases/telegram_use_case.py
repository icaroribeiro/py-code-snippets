from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.types import Update

from core.ports.inbound.telegram_port import TelegramInputPort
from core.ports.outbound.task_port import TaskServiceOutputPort
from infrastructure.cross_cutting.logging import get_logger

logger = get_logger(__name__)


class TelegramUseCase(TelegramInputPort):
    def __init__(
        self, bot: Bot, dispatcher: Dispatcher, task_service: TaskServiceOutputPort
    ) -> None:
        self._bot = bot
        self._dispatcher = dispatcher

    async def process_update(self, raw_update: dict[str, Any]) -> None:
        logger.debug("Feeding raw update payload matrix into aiogram pipeline engine.")
        telegram_update = Update.model_validate(raw_update)
        await self._dispatcher.feed_update(bot=self._bot, update=telegram_update)
