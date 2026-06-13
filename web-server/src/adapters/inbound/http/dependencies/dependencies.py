from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from core.use_cases.health_use_case import HealthUseCase
from core.use_cases.task_use_case import TaskEmailUseCase, TaskRandomNumberUseCase
from infrastructure.container import Container


class Dependencies:
    @staticmethod
    @inject
    async def health_use_case(
        health_use_case: Annotated[
            HealthUseCase,
            Depends(Provide[Container.health_use_case]),
        ],
    ) -> HealthUseCase:
        return health_use_case

    @staticmethod
    @inject
    async def task_random_number_use_case(
        task_random_number_use_case: Annotated[
            TaskRandomNumberUseCase,
            Depends(Provide[Container.task_random_number_use_case]),
        ],
    ) -> TaskRandomNumberUseCase:
        return task_random_number_use_case

    @staticmethod
    @inject
    async def task_email_use_case(
        task_email_use_case: Annotated[
            TaskEmailUseCase,
            Depends(Provide[Container.task_email_use_case]),
        ],
    ) -> TaskEmailUseCase:
        return task_email_use_case
