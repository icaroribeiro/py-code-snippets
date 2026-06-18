# core/use_cases/hello_world_use_case.py
import logging

from aiogram import Bot

logger = logging.getLogger(__name__)


class HelloWorldUseCase:
    def __init__(self, bot: Bot) -> None:
        self._bot = bot

    async def execute(self, chat_id: int) -> None:
        logger.info(f"Executing Hello World business logic for chat: {chat_id}")
        text_response = "Hello World!"
        await self._bot.send_message(chat_id=chat_id, text=text_response)
