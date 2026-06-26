from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.types import Update

from core.domain import TaskResult, TaskStatus, TaskType
from core.ports.inbound.bot_port import (
    BotTaskCallbackInputPort,
    BotWebhookInputPort,
)
from infrastructure.cross_cutting import get_logger
from infrastructure.i18n import i18nService

logger = get_logger(__name__)


class BotWebhookUseCase(BotWebhookInputPort):
    def __init__(self, bot: Bot, dispatcher: Dispatcher) -> None:
        self._bot = bot
        self._dispatcher = dispatcher

    async def process_update(self, raw_update: dict[str, Any]) -> None:
        logger.debug("Feeding raw update payload matrix into aiogram pipeline engine.")
        telegram_update = Update.model_validate(raw_update)
        await self._dispatcher.feed_update(bot=self._bot, update=telegram_update)


class BotTaskCallbackUseCase(BotTaskCallbackInputPort):
    def __init__(self, bot: Bot, i18n_service: i18nService) -> None:
        self._bot = bot
        self._i18n_service = i18n_service

    async def process_result(self, task_result: TaskResult) -> None:
        logger.info(f"Processing core callback logic for task: {task_result.task_id}")

        user_lang = task_result.lang

        if task_result.status == TaskStatus.FAILURE:
            error_msg = self._i18n_service.translate(
                key="task_error_generic", lang=user_lang
            )
            await self._bot.send_message(chat_id=task_result.chat_id, text=error_msg)
            return

        match task_result.task_type:
            case TaskType.RANDOM_NUMBER:
                generated_number = task_result.result_data.get("value", "N/A")

                message_text = self._i18n_service.translate(
                    key="task_success_random_number",
                    lang=user_lang,
                    value=generated_number,
                )

                await self._bot.send_message(
                    chat_id=task_result.chat_id,
                    text=message_text,
                    parse_mode="Markdown",
                )

            case TaskType.UNKNOWN | _:
                unknown_msg = self._i18n_service.translate(
                    key="task_type_unknown", lang=user_lang
                )
                await self._bot.send_message(
                    chat_id=task_result.chat_id, text=unknown_msg
                )
