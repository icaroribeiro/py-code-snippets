import uuid
from typing import Any, Optional

from core.domain.errors import CoreError, CoreErrorCategory
from core.domain.task import Task, TaskStatus
from core.ports.inbound.task_input_port import TaskInputPort
from core.ports.outbound.messaging.event_publisher_port import EventPublisherPort
from core.ports.outbound.persistence.task_repository_port import TaskRepositoryPort
from core.ports.outbound.task_queue.task_orchestrator_port import TaskOrchestratorPort
from infrastructure.cross_cutting.logging import get_logger

logger = get_logger(__name__)


class TaskUseCase(TaskInputPort):
    def __init__(
        self,
        repository: TaskRepositoryPort,
        orchestrator: TaskOrchestratorPort,
        publisher: EventPublisherPort,
    ) -> None:
        self._repository = repository
        self._orchestrator = orchestrator
        self._publisher = publisher

    async def create_random_number(self, payload_data: dict[str, Any]) -> Task:
        logger.info("Initiating 'create_random_number' pipeline inside Core.")
        task = await self._create_and_persist_pending_task(payload_data)
        self._orchestrator.run_background_pipeline(
            pipeline_name="create_random_number",
            task_id=task.id,
            payload_data=payload_data,
        )
        return task

    async def update_task_lifecycle_status(
        self,
        task_id: str,
        status: str,
        result: Optional[Any] = None,
        error_message: Optional[str] = None,
    ) -> Task:
        logger.info(f"Updating task {task_id} state to {status} via Core Use Case.")

        task = await self._repository.find_by_id(task_id)
        if not task:
            raise CoreError(
                f"Task {task_id} not found",
                category=CoreErrorCategory.NOT_FOUND,
            )

        if status == "PROCESSING":
            task.start_processing()
        elif status == "SUCCESS":
            task.complete(result=result)
        elif status == "FAILED":
            task.fail(error_message=error_message or "Unknown execution error")

        updated_task = await self._repository.save(task)

        if updated_task.user_id:
            channel = f"tasks:{updated_task.user_id}"
            await self._publisher.publish(
                channel, {"task_id": updated_task.id, "status": status}
            )

        return updated_task

    async def _create_and_persist_pending_task(
        self, payload_data: dict[str, Any]
    ) -> Task:
        """Centralizes entity instantiation and initial state persistence."""
        task = Task(
            id=str(uuid.uuid4()),
            status=TaskStatus.PENDING,
            payload=payload_data,
            result=None,
        )
        return await self._repository.save(task)
