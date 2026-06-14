import asyncio
import logging
import random
from typing import Any

from dependency_injector.wiring import Provide, inject

from adapters.outbound.message_queue.celery.task_lifecycle_tracker import (
    CeleryTaskLifecycleTracker,
)
from celery import Task, shared_task
from infrastructure.container import Container

logger = logging.getLogger(__name__)


class BaseTask(Task):
    """Base class for managing the execution of asynchronous tasks in Celery."""

    def __call__(self, *args, **kwargs):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()

        return loop.run_until_complete(self.run(*args, **kwargs))


@shared_task(name="create_random_number", bind=True, base=BaseTask)
@inject
async def create_random_number(
    self,
    task_id: str,
    payload_data: dict[str, Any],
    task_lifecycle_tracker: CeleryTaskLifecycleTracker = Provide[
        Container.task_lifecycle_tracker_adapter
    ],
) -> dict[str, Any]:
    """Executes the random number generation pipeline monitored by the tracker."""
    async with task_lifecycle_tracker.track_scope(celery_task=self, task_id=task_id):
        await asyncio.sleep(5)

        upper_limit = payload_data.get("number", 100)
        result_data = {
            "calculated_value": random.randint(1, upper_limit),
            "engine": "default_worker",
            "task_id": task_id,
        }

        await task_lifecycle_tracker.update_status(
            task_id=task_id, status="SUCCESS", result=result_data
        )

        return result_data
