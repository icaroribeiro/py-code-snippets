import logging

from aiogram import Bot

from core.domain.task import TaskResult, TaskStatus, TaskType
from core.ports.inbound.task_port import TaskCallbackInputPort
from infrastructure.cross_cutting.i18n_service import I18nService

logger = logging.getLogger(__name__)


class TaskCallbackUseCase(TaskCallbackInputPort):
    def __init__(self, bot: Bot, i18n_service: I18nService) -> None:
        self._bot = bot
        self._i18n_service = i18n_service

    async def execute(self, task_result: TaskResult) -> None:
        logger.info(f"Processing core callback logic for task: {task_result.task_id}")

        user_lang = task_result.lang

        if task_result.status == TaskStatus.FAILURE:
            error_msg = self._i18n_service.translate(
                "task_error_generic", lang=user_lang
            )
            await self._bot.send_message(chat_id=task_result.chat_id, text=error_msg)
            return

        match task_result.task_type:
            case TaskType.RANDOM_NUMBER:
                generated_number = task_result.result_data.get("value", "N/A")

                message_text = self._i18n_service.translate(
                    "task_success_random_number", lang=user_lang, value=generated_number
                )

                await self._bot.send_message(
                    chat_id=task_result.chat_id,
                    text=message_text,
                    parse_mode="Markdown",
                )

            case TaskType.UNKNOWN | _:
                unknown_msg = self._i18n_service.translate(
                    "task_type_unknown", lang=user_lang
                )
                await self._bot.send_message(
                    chat_id=task_result.chat_id, text=unknown_msg
                )
