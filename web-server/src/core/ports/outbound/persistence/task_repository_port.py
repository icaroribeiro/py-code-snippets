from abc import ABC, abstractmethod
from typing import Optional

from core.domain.task import Task


class TaskRepositoryPort(ABC):
    @abstractmethod
    async def save(self, task: Task) -> Task:
        pass

    @abstractmethod
    async def find_by_id(self, task_id: str) -> Optional[Task]:
        pass

    @abstractmethod
    async def find_latest_by_user(self, user_id: str) -> Optional[Task]:
        pass
