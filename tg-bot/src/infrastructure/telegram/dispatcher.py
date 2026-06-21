from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs

from adapters.inbound.telegram.features.welcome import welcome_router
from adapters.inbound.telegram.menus.bot_menu import BotMenu
from adapters.inbound.telegram.middlewares.language_middleware import LanguageMiddleware
from infrastructure.cross_cutting.logging import get_logger

logger = get_logger(__name__)


class TelegramDispatcher:
    def __init__(self, bot_menu: BotMenu) -> None:
        self._bot_menu = bot_menu

    def init(self) -> Dispatcher:
        dp = Dispatcher()
        dp.startup.register(self._bot_menu.register_all)
        # dp["hello_world_use_case"] = hello_world_use_case
        # dp.include_router(hello_world_router)
        dp.message.middleware(LanguageMiddleware())
        dp.include_router(welcome_router)
        setup_dialogs(dp)
        return dp
