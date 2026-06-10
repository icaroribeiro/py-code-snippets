import asyncio
from contextlib import contextmanager
from typing import Any, Generator

from core.use_cases.task_use_case import TaskUseCase


@contextmanager
def task_lifecycle_scope(
    task: Any, task_id: str, use_case: TaskUseCase
) -> Generator[None, None, None]:
    try:
        asyncio.run(
            use_case.update_task_lifecycle_status(task_id=task_id, status="PROCESSING")
        )
        yield
    except Exception as error:
        asyncio.run(
            use_case.update_task_lifecycle_status(
                task_id=task_id, status="FAILED", error_message=str(error)
            )
        )
        raise task.retry(exc=error, countdown=10)
