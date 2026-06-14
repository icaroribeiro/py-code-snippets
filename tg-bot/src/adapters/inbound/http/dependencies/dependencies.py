from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from core.use_cases.health_use_case import HealthCheckUseCase
from core.use_cases.telegram_use_case import TelegramUseCase
from infrastructure.container import Container


class Dependencies:
    @staticmethod
    @inject
    async def health_check_use_case(
        health_check_use_case: Annotated[
            HealthCheckUseCase,
            Depends(Provide[Container.health_check_use_case]),
        ],
    ) -> HealthCheckUseCase:
        return health_check_use_case

    @staticmethod
    @inject
    async def telegram_use_case(
        telegram_use_case: Annotated[
            TelegramUseCase,
            Depends(Provide[Container.telegram_use_case]),
        ],
    ) -> TelegramUseCase:
        return telegram_use_case
