from abc import ABC, abstractmethod
from typing import Any

from core.domain.task import Task


class TaskRandomNumberInputPort(ABC):
    @abstractmethod
    async def create_random_number(self, payload_data: dict[str, Any]) -> Task:
        pass


class TaskEmailInputPort(ABC):
    @abstractmethod
    async def send_email(self, payload_data: dict[str, Any]) -> Task:
        pass
