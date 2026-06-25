from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs

from infrastructure.cross_cutting import get_logger
from infrastructure.i18n import i18nService
from telegram.features import features_router
from telegram.menu import TelegramMenu
from telegram.middlewares.language_middleware import LanguageMiddleware

logger = get_logger(__name__)


class TelegramDispatcher:
    def __init__(self, menu: TelegramMenu, i18n_service: i18nService) -> None:
        self._menu = menu
        self._i18n_service = i18n_service

    def init(self) -> Dispatcher:
        dp = Dispatcher()

        dp["i18n_service"] = self._i18n_service

        dp.startup.register(self._menu.set_commands)

        dp.message.middleware(LanguageMiddleware())

        dp.include_router(features_router)

        setup_dialogs(dp)

        return dp
