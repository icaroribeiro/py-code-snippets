from typing import Annotated

from aiogram import Bot
from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from core.ports.inbound.health_port import HealthCheckInputPort
from core.ports.inbound.task_callback_port import TaskCallbackInputPort
from core.ports.inbound.telegram_port import TelegramInputPort
from infrastructure.container import Container


class Dependencies:
    @staticmethod
    @inject
    async def health_check_use_case(
        health_check_use_case: Annotated[
            HealthCheckInputPort,
            Depends(Provide[Container.health_check_use_case]),
        ],
    ) -> HealthCheckInputPort:
        return health_check_use_case

    @staticmethod
    @inject
    async def telegram_use_case(
        telegram_use_case: Annotated[
            TelegramInputPort,
            Depends(Provide[Container.telegram_use_case]),
        ],
    ) -> TelegramInputPort:
        return telegram_use_case

    @staticmethod
    @inject
    async def task_callback_use_case(
        task_callback_use_case: TaskCallbackInputPort = Depends(
            Provide[Container.task_callback_use_case]
        ),
    ) -> TaskCallbackInputPort:
        return task_callback_use_case

    @staticmethod
    @inject
    async def bot(
        bot: Annotated[
            Bot,
            Depends(Provide[Container.bot]),
        ],
    ) -> Bot:
        return bot
