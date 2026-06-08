import uuid
from typing import Any, Coroutine, Optional

from core.domain.errors import CoreError, CoreErrorCategory
from core.domain.task import Task, TaskStatus
from core.ports.inbound.task_input_port import TaskInputPort
from core.ports.outbound.messaging.event_publisher_port import EventPublisherPort
from core.ports.outbound.persistence.task_repository_port import TaskRepositoryPort
from core.ports.outbound.task_queue.task_manager_port import TaskManagerPort
from infrastructure.logging import get_logger

logger = get_logger(__name__)


class TaskUseCase(TaskInputPort):
    def __init__(
        self,
        repository: TaskRepositoryPort,
        publisher: EventPublisherPort,
        manager: TaskManagerPort,
    ) -> None:
        self._repository = repository
        self._publisher = publisher
        self._manager = manager

    async def create_random_number(self, payload_data: dict[str, Any]) -> Task:
        """
        Inbound Port Implementation.
        Generates the unique identity tracker and offloads processing to Celery.
        """
        logger.info("Initiating 'create_random_number' pipeline inside Core.")

        generated_id = str(uuid.uuid4())
        task = Task(
            id=generated_id,
            status=TaskStatus.PENDING,
            payload=payload_data,
            result=None,
        )

        # Salva o estado inicial PENDING no banco antes de despachar para a fila
        await self._repository.save(task)

        # Importação tardia (Lazy Import) para evitar dependência cíclica de infraestrutura
        from infrastructure.celery.tasks.create_random_number_task import (
            trigger_create_random_number_task,
        )

        trigger_create_random_number_task.delay(  # type: ignore[attr-defined]
            task_id=generated_id, payload_data=payload_data
        )

        return task

    async def execute_task_pipeline(
        self, task_id: str, task_name: str, async_coro: Coroutine[Any, Any, Any]
    ) -> Any:
        """
        Agnostic Core Orchestrator.
        Intercepts execution from ANY background task infrastructure to handle state
        transitions, persistence, and event broadcasting inside the domain.
        """
        logger.info(
            f"Orchestrating pipeline execution for task [{task_name}] (ID: {task_id})"
        )

        try:
            # 1. Transiciona atomicamente para PROCESSING
            await self._update_task_status(task_id=task_id, status="PROCESSING")

            # 2. Executa a função/corrotina real contendo as regras de negócio da tarefa
            result_data = await async_coro

            # 3. Se finalizar com sucesso, salva o resultado e altera o status para SUCCESS
            await self._update_task_status(
                task_id=task_id, status="SUCCESS", result=result_data
            )
            return result_data

        except Exception as error:
            logger.error(
                f"Failure during core execution of task [{task_name}] (ID: {task_id}): {str(error)}"
            )

            # 4. Em caso de qualquer erro na corrotina, garante a persistência do estado FAILED
            await self._update_task_status(
                task_id=task_id,
                status="FAILED",
                error_message=f"Task execution failure: {str(error)}",
            )
            raise error

    async def _update_task_status(
        self,
        task_id: str,
        status: str,
        result: Optional[Any] = None,
        error_message: Optional[str] = None,
    ) -> Task:
        """
        Private domain utility to centralize database state persistence
        and downstream message streaming (Pub/Sub notifications).
        """
        logger.info(
            f"Updating task {task_id} status to {status} via core orchestrator."
        )

        task = await self._repository.find_by_id(task_id)
        if not task:
            raise CoreError(
                f"Task {task_id} not found",
                category=CoreErrorCategory.NOT_FOUND,
            )

        # Mutação baseada puramente nos métodos ricos expostos na sua Dataclass de domínio
        if status == "PROCESSING":
            task.start_processing()
        elif status == "SUCCESS":
            task.complete(result=result)
        elif status == "FAILED":
            task.fail(error_message=error_message or "Unknown execution error")

        updated_task = await self._repository.save(task)

        # Se houver um usuário atrelado à tarefa, notifica o canal via Redis/EventPublisher
        if updated_task.user_id:
            channel = f"tasks:{updated_task.user_id}"
            await self._publisher.publish(
                channel, {"task_id": updated_task.id, "status": status}
            )

        return updated_task
