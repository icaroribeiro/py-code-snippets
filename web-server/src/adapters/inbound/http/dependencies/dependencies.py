from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from core.use_cases.health_use_case import HealthUseCase
from core.use_cases.task_use_case import TaskUseCase
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
    async def task_use_case(
        task_use_case: Annotated[
            TaskUseCase,
            Depends(Provide[Container.task_use_case]),
        ],
    ) -> TaskUseCase:
        return task_use_case
