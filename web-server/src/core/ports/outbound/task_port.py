from abc import ABC, abstractmethod
from typing import Any, Optional

from core.domain.task import Task


class TaskRepositoryOutputPort(ABC):
    @abstractmethod
    async def save(self, task: Task) -> Task:
        pass

    @abstractmethod
    async def find_by_id(self, task_id: str) -> Optional[Task]:
        pass


class TaskEventPublisherOutputPort(ABC):
    @abstractmethod
    async def publish(self, channel: str, message: dict[str, Any]) -> None:
        pass


class TaskOrchestratorOutputPort(ABC):
    @abstractmethod
    async def initialize_and_start(
        self, pipeline_name: str, payload_data: dict[str, Any]
    ) -> Task:
        pass
