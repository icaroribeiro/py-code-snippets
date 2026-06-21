from abc import ABC, abstractmethod
from typing import Any


class TaskServiceApiOutputPort(ABC):
    @abstractmethod
    async def forward_task(self, payload: dict[str, Any]) -> dict[str, Any]:
        pass
