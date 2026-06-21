from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs

from adapters.inbound.telegram.features.welcome import welcome_dialog, welcome_router
from adapters.inbound.telegram.menus.bot_menu import TelegramBotMenu
from adapters.inbound.telegram.middlewares.language_middleware import LanguageMiddleware
from infrastructure.cross_cutting.logging import get_logger
from infrastructure.i18n.localization_service import LocalizationService

logger = get_logger(__name__)


class TelegramDispatcher:
    def __init__(
        self, bot_menu: TelegramBotMenu, localization_service: LocalizationService
    ) -> None:
        self._bot_menu = bot_menu
        self._localization_service = localization_service

    def init(self) -> Dispatcher:
        dp = Dispatcher()
        dp["localization_service"] = self._localization_service

        # 1. Lifecycle and Global Menu
        dp.startup.register(self._bot_menu.register_all)

        # 2. Global Middlewares
        dp.message.middleware(LanguageMiddleware())

        # 3. Command Routers and Visual Dialogs
        dp.include_router(welcome_router)
        dp.include_router(welcome_dialog)

        # 4. Final Setup of Dialogs Framework
        setup_dialogs(dp)

        return dp
