from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from core.ports.inbound.health_port import HealthCheckInputPort
from core.ports.inbound.telegram_port import (
    TelegramTaskCallbackInputPort,
    TelegramWebhookInputPort,
)
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
    async def telegram_webhook_use_case(
        telegram_webhook_use_case: Annotated[
            TelegramWebhookInputPort,
            Depends(Provide[Container.telegram_webhook_use_case]),
        ],
    ) -> TelegramWebhookInputPort:
        return telegram_webhook_use_case

    @staticmethod
    @inject
    async def telegram_task_callback_use_case(
        telegram_task_callback_use_case: TelegramTaskCallbackInputPort = Depends(
            Provide[Container.telegram_task_callback_use_case]
        ),
    ) -> TelegramTaskCallbackInputPort:
        return telegram_task_callback_use_case

    # @staticmethod
    # @inject
    # async def bot(
    #     bot: Annotated[
    #         Bot,
    #         Depends(Provide[Container.bot]),
    #     ],
    # ) -> Bot:
    #     return bot
