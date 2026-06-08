from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


@dataclass
class Task:
    """
    dataclass without frozen=True here just because the business rules exposed
    in the methods change the internal state of the task throughout its lifecycle
    """

    id: str
    status: TaskStatus = TaskStatus.PENDING
    payload: dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None
    # Traceability and Delivery Context
    user_id: Optional[str] = None  # e.g.: "telegram|55329182" ou "user_123"
    metadata: dict[str, Any] = field(
        default_factory=dict
    )  # e.g.: {"chat_id": 998231, "platform": "telegram"}
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def start_processing(self) -> None:
        self.status = TaskStatus.PROCESSING
        self.updated_at = datetime.now(timezone.utc)

    def complete(self, result: Any) -> None:
        self.status = TaskStatus.SUCCESS
        self.result = result
        self.updated_at = datetime.now(timezone.utc)

    def fail(self, error_message: str) -> None:
        self.status = TaskStatus.FAILED
        self.result = {"error": error_message}
        self.updated_at = datetime.now(timezone.utc)
