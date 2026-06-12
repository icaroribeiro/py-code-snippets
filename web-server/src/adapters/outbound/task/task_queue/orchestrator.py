from typing import Any

from celery import signature

from core.ports.outbound.task.task_queue.orchestrator_output_port import (
    TaskOrchestratorOutputPort,
)


class TaskOrchestrator(TaskOrchestratorOutputPort):
    def run_background_pipeline(
        self, pipeline_name: str, task_id: str, payload_data: dict[str, Any]
    ) -> None:
        match pipeline_name:
            case "create_random_number":
                signature(
                    "tasks.create_random_number", args=[task_id, payload_data]
                ).delay()  # type: ignore[attr-defined]
            case "send_invoice":
                # Exemplo de expansão futura simplificada:
                # from adapters.outbound.task_queue.tasks.send_invoice_task import trigger_send_invoice_task
                # trigger_send_invoice_task.delay(task_id=task_id, payload_data=payload_data)
                pass

            case _:
                raise ValueError(
                    f"Unknown background pipeline registry: {pipeline_name}"
                )
