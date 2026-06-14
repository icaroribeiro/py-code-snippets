from typing import Any, Optional

from pydantic import BaseModel, Field

from core.domain.task import Task


class TaskResponseSchema(BaseModel):
    task_id: str = Field(...)
    status: str = Field(...)
    result: Optional[Any] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)


class TaskMapper:
    def __init__(self) -> None:
        pass

    @staticmethod
    def domain_to_response(domain: Task) -> TaskResponseSchema:
        """
        Maps the pure domain  task entity to the HTTP Inbound Response Schema.
        Used strictly at the API controller border.
        """
        return TaskResponseSchema(
            task_id=domain.id,
            status=domain.status.value
            if hasattr(domain.status, "value")
            else str(domain.status),
            result=domain.result,
            updated_at=domain.updated_at.isoformat().replace("+00:00", "") + "Z"
            if domain.updated_at
            else None,
        )
