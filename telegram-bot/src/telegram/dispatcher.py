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
        dispatcher = Dispatcher()
        dispatcher["i18n_service"] = self._i18n_service
        dispatcher.startup.register(self._menu.set_commands)
        dispatcher.message.middleware(LanguageMiddleware())
        dispatcher.include_router(features_router)

        setup_dialogs(dispatcher)

        return dispatcher
