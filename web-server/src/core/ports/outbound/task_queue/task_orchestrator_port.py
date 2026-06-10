from abc import ABC, abstractmethod
from typing import Any


class TaskOrchestratorPort(ABC):
    @abstractmethod
    def run_background_pipeline(
        self, pipeline_name: str, task_id: str, payload_data: dict[str, Any]
    ) -> None:
        pass
