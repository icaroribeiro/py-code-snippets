from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from core.ports.inbound.bot_port import (
    BotTaskCallbackInputPort,
    BotWebhookInputPort,
)
from core.ports.inbound.health_port import HealthCheckInputPort
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
    async def bot_webhook_use_case(
        bot_webhook_use_case: Annotated[
            BotWebhookInputPort,
            Depends(Provide[Container.bot_webhook_use_case]),
        ],
    ) -> BotWebhookInputPort:
        return bot_webhook_use_case

    @staticmethod
    @inject
    async def bot_task_callback_use_case(
        bot_task_callback_use_case: BotTaskCallbackInputPort = Depends(
            Provide[Container.bot_task_callback_use_case]
        ),
    ) -> BotTaskCallbackInputPort:
        return bot_task_callback_use_case
