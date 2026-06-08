import asyncio
from abc import ABC, abstractmethod
from typing import Any

from celery import Task as CeleryTask

from infrastructure.logging import get_logger

logger = get_logger(__name__)


class BaseTask(CeleryTask, ABC):
    """
    Abstract Base Task that resolves its own Inbound Ports
    at the Worker's infrastructure layer upon instantiation.
    """

    abstract = True

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    async def run_async(self, task_id: str, payload_data: dict[str, Any]) -> Any:
        """Must be implemented by child tasks for specific business logic."""
        pass

    def run(
        self, task_id: str, payload_data: dict[str, Any], *args: Any, **kwargs: Any
    ) -> Any:
        """Orchestrates states using the injected Inbound Port."""
        logger.info(f"Worker executing task [{self.name}] for ID: {task_id}")

        async def _execute_pipeline() -> Any:
            try:
                # Usa a dependência injetada no __init__ do Worker de forma limpa
                await self._update_task_use_case.execute(
                    task_id=task_id, status="PROCESSING"
                )

                result_data = await self.run_async(
                    task_id=task_id, payload_data=payload_data
                )

                await self._update_task_use_case.execute(
                    task_id=task_id, status="SUCCESS", result=result_data
                )
                return result_data

            except Exception as error:
                logger.error(
                    f"Failure on task [{self.name}] (ID: {task_id}): {str(error)}"
                )
                await self._update_task_use_case.execute(
                    task_id=task_id,
                    status="FAILED",
                    error_message=f"Worker failure: {str(error)}",
                )
                raise self.retry(exc=error, countdown=10)

        return asyncio.run(_execute_pipeline())
