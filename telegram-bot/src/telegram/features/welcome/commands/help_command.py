from aiogram.types import BotCommand

from infrastructure.i18n import i18nService
from telegram.features.welcome.constants.i18n import CMD_HELP_KEY


class HelpCommand:
    def __init__(self, i18n_service: i18nService) -> None:
        self._i18n_service = i18n_service

    def build(self, lang: str) -> BotCommand:
        return BotCommand(
            command="/help",
            description=self._i18n_service.translate(key=CMD_HELP_KEY, lang=lang),
        )
