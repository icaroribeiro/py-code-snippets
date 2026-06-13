import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Optional

from core.domain.errors import CoreError, CoreErrorCategory
from core.domain.task import Task as DomainTask
from core.ports.outbound.task_port import (
    TaskEventPublisherOutputPort,
    TaskRepositoryOutputPort,
)

logger = logging.getLogger(__name__)


class TaskLifecycleTracker:
    def __init__(
        self,
        task_repository: TaskRepositoryOutputPort,
        task_event_publisher: TaskEventPublisherOutputPort,
    ) -> None:
        self._task_repository = task_repository
        self._task_event_publisher = task_event_publisher

    async def update_status(
        self,
        task_id: str,
        status: str,
        result: Optional[Any] = None,
        error_message: Optional[str] = None,
    ) -> DomainTask:
        """Updates the database state and publishes events to listeners."""
        logger.info(f"Tracking state transition to {status} for task {task_id}")

        task = await self._task_repository.find_by_id(task_id)
        if not task:
            raise CoreError(
                f"Task {task_id} not found during tracking lifecycle update",
                category=CoreErrorCategory.NOT_FOUND,
            )

        if status == "PROCESSING":
            task.start_processing()
        elif status == "SUCCESS":
            task.complete(result=result)
        elif status == "FAILED":
            task.fail(error_message=error_message or "Unknown execution error")

        updated_task = await self._task_repository.save(task)

        if updated_task.user_id:
            channel = f"tasks:{updated_task.user_id}"
            await self._task_event_publisher.publish(
                channel, {"task_id": updated_task.id, "status": status}
            )

        return updated_task

    @asynccontextmanager
    async def track_scope(
        self, celery_task: Any, task_id: str
    ) -> AsyncGenerator[None, None]:
        """Context manager to automate PROCESSING and FAILED boundary transitions safely."""
        try:
            await self.update_status(task_id=task_id, status="PROCESSING")
            yield
        except Exception as error:
            logger.error(f"Task context crashed on {task_id}. Error: {error}")
            await self.update_status(
                task_id=task_id, status="FAILED", error_message=str(error)
            )
            raise celery_task.retry(exc=error, countdown=10)
