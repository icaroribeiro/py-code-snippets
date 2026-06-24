from typing import Any

from core.domain.task import Task
from core.ports.inbound.task_port import TaskEmailInputPort, TaskRandomNumberInputPort
from core.ports.outbound import (
    TaskOrchestratorOutputPort,
)
from infrastructure.cross_cutting import get_logger

logger = get_logger(__name__)


class TaskRandomNumberUseCase(TaskRandomNumberInputPort):
    def __init__(self, task_orchestrator: TaskOrchestratorOutputPort) -> None:
        self._task_orchestrator = task_orchestrator

    async def create_random_number(self, payload_data: dict[str, Any]) -> Task:
        logger.info(
            "Initiating 'create_random_number' pipeline via specialized orchestrator."
        )
        return await self._task_orchestrator.initialize_and_start(
            pipeline_name="create_random_number", payload_data=payload_data
        )


class TaskEmailUseCase(TaskEmailInputPort):
    def __init__(self, task_orchestrator: TaskOrchestratorOutputPort) -> None:
        self._task_orchestrator = task_orchestrator

    async def send_email(self, payload_data: dict[str, Any]) -> Task:
        logger.info("Initiating 'send_email' pipeline via specialized orchestrator.")
        return await self._task_orchestrator.initialize_and_start(
            pipeline_name="send_email", payload_data=payload_data
        )
