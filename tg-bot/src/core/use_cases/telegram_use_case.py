from aiogram import Bot, Dispatcher

from core.ports.inbound.telegram_port import TelegramInputPort
from infrastructure.cross_cutting.logging import get_logger

logger = get_logger(__name__)


class TelegramUseCase(TelegramInputPort):
    def __init__(self) -> None:
        pass

    async def foo(
        self, json_data: dict[str, Any], bot: Bot | None, dispatcher: Dispatcher | None
    ) -> None:
        pass
