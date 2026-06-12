import asyncio
import random
from typing import Any

from celery import Task, shared_task
from dependency_injector.wiring import Provide, inject

from adapters.outbound.task.task_queue.lifecycle_scope import task_lifecycle_scope
from core.use_cases.task.use_case import TaskUseCase
from infrastructure.container import Container


class BaseTask(Task):
    """Base class for managing the execution of asynchronous tasks in Celery."""

    def __call__(self, *args, **kwargs):
        # Gets the existing and active event loop in the Worker's process
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()

        # Runs the native coroutine until it finishes, using the correct loop
        return loop.run_until_complete(self.run(*args, **kwargs))


class CreateRandomNumberTask:
    async def do_work(self, task_id: str, payload_data: dict[str, Any]):
        await asyncio.sleep(5)

        upper_limit = payload_data.get("number", 100)
        result_data = {
            "calculated_value": random.randint(1, upper_limit),
            "engine": "default_worker",
            "task_id": task_id,
        }

        return result_data


@shared_task(name="create_random_number", bind=True, base=BaseTask)
@inject
async def create_random_number(
    self,
    task_id: str,
    payload_data: dict[str, Any],
    use_case: TaskUseCase = Provide[Container.task_use_case],
) -> dict:
    # Using 'async with' natively binds everything to the correct worker event loop
    async with task_lifecycle_scope(task=self, task_id=task_id, use_case=use_case):
        task = CreateRandomNumberTask()
        result_data = await task.do_work(task_id=task_id, payload_data=payload_data)
        # Directly await the success database persistence
        await use_case.update_task_lifecycle_status(
            task_id=task_id, status="SUCCESS", result=result_data
        )
        return result_data
