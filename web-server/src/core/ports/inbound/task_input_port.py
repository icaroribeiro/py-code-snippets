from abc import ABC, abstractmethod
from typing import Any

from core.domain.task import Task


class TaskInputPort(ABC):
    @abstractmethod
    async def create_random_number(self, payload_data: dict[str, Any]) -> Task:
        pass
