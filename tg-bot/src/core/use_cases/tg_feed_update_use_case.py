from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.types import Update

from core.ports.inbound.webhook_port import TgFeedUpdateInputPort
from infrastructure.cross_cutting.logging import get_logger

logger = get_logger(__name__)


class TgFeedUpdateUseCase(TgFeedUpdateInputPort):
    def __init__(self, bot: Bot, dispatcher: Dispatcher) -> None:
        self._bot = bot
        self._dispatcher = dispatcher

    async def process_update(self, raw_update: dict[str, Any]) -> None:
        logger.debug("Feeding raw update payload matrix into aiogram pipeline engine.")
        telegram_update = Update.model_validate(raw_update)
        await self._dispatcher.feed_update(bot=self._bot, update=telegram_update)
