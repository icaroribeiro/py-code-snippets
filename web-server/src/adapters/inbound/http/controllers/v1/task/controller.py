from fastapi import APIRouter, Depends, status

from adapters.inbound.http.controllers.v1.task.mapper import (
    TaskMapper,
    TaskResponseSchema,
)
from adapters.inbound.http.dependencies.dependencies import Dependencies
from core.use_cases.task.use_case import TaskUseCase

router = APIRouter(prefix="/tasks")


@router.post(
    "/random-number",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TaskResponseSchema,
    summary="Create a random number task",
)
async def create_random_number(
    payload: dict,
    task_use_case: TaskUseCase = Depends(Dependencies.task_use_case),
) -> TaskResponseSchema:
    task_domain = await task_use_case.create_random_number(payload_data=payload)

    return TaskMapper.domain_to_response(task_domain)
