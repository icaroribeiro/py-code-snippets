from typing import Any

from pydantic import BaseModel, Field

from core.domain import TaskResult, TaskStatus, TaskType


class TelegramWebhookMapper:
    @staticmethod
    def request_to_domain_dict(raw_json: dict[str, Any]) -> dict[str, Any]:
        """Maps HTTP incoming request body payload to core system-executable dictionary format."""
        return raw_json


class TelegramTaskCallbackRequestSchema(BaseModel):
    task_id: str = Field(...)
    task_type: str = Field(...)
    chat_id: int = Field(...)
    status: str = Field(...)
    result: dict[str, Any] = Field(default_factory=dict)
    lang: str = Field(...)


class TelegramTaskCallbackMapper:
    @staticmethod
    def request_to_domain(
        request: TelegramTaskCallbackRequestSchema,
    ) -> TaskResult:
        try:
            t_type = TaskType(request.task_type)
        except ValueError:
            t_type = TaskType.UNKNOWN

        try:
            t_status = TaskStatus(request.status.lower())
        except ValueError:
            t_status = TaskStatus.FAILURE

        return TaskResult(
            task_id=request.task_id,
            task_type=t_type,
            chat_id=request.chat_id,
            status=t_status,
            result_data=request.result,
            lang=request.lang,
        )
