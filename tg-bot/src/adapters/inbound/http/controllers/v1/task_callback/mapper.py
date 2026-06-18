from typing import Any

from pydantic import BaseModel, Field

from core.domain.task import TaskResult, TaskStatus, TaskType


class TaskCallbackRequestSchema(BaseModel):
    task_id: str = Field(...)
    task_type: str = Field(...)
    chat_id: int = Field(...)
    status: str = Field(...)
    result: dict[str, Any] = Field(default_factory=dict)
    lang: str = Field(...)


class TaskCallbackMapper:
    @staticmethod
    def request_to_domain(request: TaskCallbackRequestSchema) -> TaskResult:
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
