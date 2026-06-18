from abc import ABC, abstractmethod

from core.domain.task import TaskResult


class TaskCallbackInputPort(ABC):
    @abstractmethod
    async def execute(self, task_result: TaskResult) -> None:
        """Executes the business logic for a completed background task."""
        pass
