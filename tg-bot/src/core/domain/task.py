from dataclasses import dataclass
from enum import Enum
from typing import Any


class TaskStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class TaskType(str, Enum):
    RANDOM_NUMBER = "random_number"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class TaskResult:
    task_id: str
    task_type: TaskType
    chat_id: int
    status: TaskStatus
    lang: str
    result_data: dict[str, Any]
