from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv

from adapters.inbound.http.controllers.v1.task.mapper import (
    TaskMapper,
    TaskResponseSchema,
)
from adapters.inbound.http.dependencies.dependencies import Dependencies
from core.use_cases.task_use_case import TaskEmailUseCase, TaskRandomNumberUseCase

router = APIRouter(prefix="/tasks")


@cbv(router)
class TaskController:
    task_random_number_use_case: TaskRandomNumberUseCase = Depends(
        Dependencies.task_random_number_use_case
    )
    task_email_use_case: TaskEmailUseCase = Depends(Dependencies.task_email_use_case)

    @router.post(
        "/random-numbers",
        status_code=status.HTTP_202_ACCEPTED,
        response_model=TaskResponseSchema,
        summary="Create a random number",
    )
    async def create_random_number(
        self,
        payload: dict,
    ) -> TaskResponseSchema:
        task_domain = await self.task_random_number_use_case.create_random_number(
            payload_data=payload
        )

        return TaskMapper.domain_to_response(task_domain)

    @router.post(
        "/emails",
        status_code=status.HTTP_202_ACCEPTED,
        response_model=TaskResponseSchema,
        summary="Send email",
    )
    async def send_email(self, payload: dict) -> TaskResponseSchema:
        task_domain = await self.task_email_use_case.send_email(payload_data=payload)

        return TaskMapper.domain_to_response(task_domain)
