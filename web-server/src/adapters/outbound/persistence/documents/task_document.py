from datetime import datetime, timezone
from typing import Annotated, Any, Optional

from beanie import Document, Indexed
from pydantic import Field

from core.domain.task import TaskStatus


class TaskDocument(Document):
    status: Annotated[str, Indexed(str)] = TaskStatus.PENDING.value
    payload: dict[str, Any] = Field(default_factory=dict)
    result: Optional[Any] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "tasks"
        indexes = [
            "status",
            "created_at",
            [("status", 1), ("created_at", -1)],
        ]
