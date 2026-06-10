import asyncio
import random
from typing import Any

from celery import shared_task
from dependency_injector.wiring import Provide, inject

from adapters.outbound.task_queue.task_lifecycle_scope import task_lifecycle_scope
from adapters.outbound.task_queue.tasks.base_task import BaseTask
from core.use_cases.task_use_case import TaskUseCase
from infrastructure.container import Container


@shared_task(name="tasks.create_random_number", bind=True, base=BaseTask)
@inject
async def trigger_create_random_number_task(
    self,
    task_id: str,
    payload_data: dict[str, Any],
    use_case: TaskUseCase = Provide[Container.task_use_case],
) -> dict:

    # Using 'async with' natively binds everything to the correct worker event loop
    async with task_lifecycle_scope(task=self, task_id=task_id, use_case=use_case):
        # Native, non-blocking async sleep
        await asyncio.sleep(5)

        upper_limit = payload_data.get("number", 100)
        result_data = {
            "calculated_value": random.randint(1, upper_limit),
            "engine": "default_worker",
            "task_id": task_id,
        }

        # Directly await the success database persistence
        await use_case.update_task_lifecycle_status(
            task_id=task_id, status="SUCCESS", result=result_data
        )

        return result_data
