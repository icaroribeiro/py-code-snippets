from fastapi import APIRouter, Depends, Response, status

from adapters.inbound.http.controllers.v1.task.mapper import (
    TaskCallbackMapper,
    TaskCallbackRequestSchema,
)
from adapters.inbound.http.dependencies.dependencies import Dependencies
from core.ports.inbound.task_port import TaskCallbackInputPort
from infrastructure.cross_cutting.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/tasks")


@router.post("/callbacks", status_code=status.HTTP_200_OK)
async def handle_task_callback(
    payload: TaskCallbackRequestSchema,
    response: Response,
    task_callback_use_case: TaskCallbackInputPort = Depends(
        Dependencies.task_callback_use_case
    ),
) -> Response:
    logger.info(f"Callback HTTP hit for task_id: {payload.task_id}")
    task_domain = TaskCallbackMapper.request_to_domain(payload)

    await task_callback_use_case.execute(task_domain)

    return response
