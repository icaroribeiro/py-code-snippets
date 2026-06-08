import asyncio
import random
from typing import Any

from celery import shared_task
from dependency_injector.wiring import Provide, inject

from core.use_cases.task_use_case import TaskUseCase
from infrastructure.container import Container


@shared_task(
    name="tasks.create_random_number_task",
    bind=True,
    max_retries=3,
)
@inject
def trigger_create_random_number_task(
    self,
    task_id: str,
    payload_data: dict[str, Any],
    use_case: TaskUseCase = Provide[Container.task_use_case],
) -> dict:
    """
    Unified Celery Task. Orchestrates the lifecycle state transitions and
    runs the core business logic inside a single execution context.
    """

    async def _execute_and_calculate() -> dict[str, Any]:
        # 1. Executa o delay simulado
        await asyncio.sleep(5)

        # 2. Processa a lógica de negócio do limite numérico
        upper_limit = payload_data.get("number", 100)

        return {
            "calculated_value": random.randint(1, upper_limit),
            "engine": "default_worker",
            "task_id": task_id,
        }

    try:
        # Repassa a corrotina local diretamente para o orquestrador do Caso de Uso
        return asyncio.run(
            use_case.execute_task_pipeline(
                task_id=task_id,
                task_name="create_random_number",
                async_coro=_execute_and_calculate(),
            )
        )
    except Exception as error:
        # Garante que falhas de infraestrutura/transporte permitam o retry do Celery
        raise self.retry(exc=error, countdown=10)
