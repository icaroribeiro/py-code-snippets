import uuid
from typing import Any

from celery import signature
from core.domain.task import Task, TaskStatus
from core.ports.outbound.task_port import (
    TaskOrchestratorOutputPort,
    TaskRepositoryOutputPort,
)
from infrastructure.cross_cutting.logging import get_logger

logger = get_logger(__name__)


class CeleryTaskOrchestrator(TaskOrchestratorOutputPort):
    def __init__(self, task_repository: TaskRepositoryOutputPort) -> None:
        self._task_repository = task_repository

    async def initialize_and_start(
        self, pipeline_name: str, payload_data: dict[str, Any]
    ) -> Task:
        """Centralizes entity creation in the database and background queue triggering."""
        logger.info(f"Orchestrating startup pipeline for task type: '{pipeline_name}'")

        task = Task(
            id=str(uuid.uuid4()),
            status=TaskStatus.PENDING,
            payload=payload_data,
            result=None,
        )
        saved_task = await self._task_repository.save(task)

        self._run_background_pipeline(
            pipeline_name=pipeline_name,
            task_id=saved_task.id,
            payload_data=payload_data,
        )

        return saved_task

    def _run_background_pipeline(
        self, pipeline_name: str, task_id: str, payload_data: dict[str, Any]
    ) -> None:
        """Private mapper that triggers native Celery signatures."""
        match pipeline_name:
            case "create_random_number":
                signature(
                    "tasks.create_random_number", args=[task_id, payload_data]
                ).delay()  # type: ignore[attr-defined]
            case "send_email":
                signature("tasks.send_email", args=[task_id, payload_data]).delay()  # type: ignore[attr-defined]
            case _:
                raise ValueError(
                    f"Unknown background pipeline registry: {pipeline_name}"
                )
