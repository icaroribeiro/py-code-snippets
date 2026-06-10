import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from core.use_cases.task_use_case import TaskUseCase

logger = logging.getLogger(__name__)


@asynccontextmanager
async def task_lifecycle_scope(
    task: Any, task_id: str, use_case: TaskUseCase
) -> AsyncGenerator[None, None]:
    """
    Asynchronous context manager to orchestrate Celery task lifecycle states.
    Since the task runs natively within an async context (AsyncTask), we can
    directly await the Use Case operations without manipulating the event loop.
    """
    try:
        # 1. Seamlessly await the PROCESSING state transition
        logger.info(f"Updating task {task_id} state to PROCESSING via Core Use Case.")
        await use_case.update_task_lifecycle_status(
            task_id=task_id, status="PROCESSING"
        )

        # Yield control back to the async Celery task body
        yield

    except Exception as error:
        logger.error(f"Task {task_id} failed. Updating state to FAILED. Error: {error}")

        # 2. Seamlessly await the FAILED state transition on exception
        await use_case.update_task_lifecycle_status(
            task_id=task_id, status="FAILED", error_message=str(error)
        )

        # 3. Trigger Celery's native retry mechanism
        raise task.retry(exc=error, countdown=10)
