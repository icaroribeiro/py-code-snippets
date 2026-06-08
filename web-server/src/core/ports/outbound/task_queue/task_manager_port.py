from abc import ABC, abstractmethod
from typing import Any


class TaskManagerPort(ABC):
    @abstractmethod
    async def foo(self) -> Any:
        pass
