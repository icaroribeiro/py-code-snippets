from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs

from infrastructure.cross_cutting import get_logger, i18nService
from telegram.bot_menu import TelegramBotMenu
from telegram.features.welcome import welcome_router
from telegram.middlewares.language_middleware import LanguageMiddleware

logger = get_logger(__name__)


class TelegramDispatcher:
    def __init__(self, bot_menu: TelegramBotMenu, i18n_service: i18nService) -> None:
        self._bot_menu = bot_menu
        self._i18n_service = i18n_service

    def init(self) -> Dispatcher:
        dp = Dispatcher()
        dp["i18n_service"] = self._i18n_service
        dp.startup.register(self._bot_menu.set_commands)
        dp.message.middleware(LanguageMiddleware())
        dp.include_router(welcome_router)
        # dp.include_router(welcome_dialog)
        setup_dialogs(dp)
        return dp
