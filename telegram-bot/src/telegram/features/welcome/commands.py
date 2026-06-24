from aiogram.types import BotCommand

from infrastructure.cross_cutting import i18nService


class WelcomeCommands:
    def __init__(self, i18n_service: i18nService) -> None:
        self._i18n_service = i18n_service

    def get_commands(self, lang: str) -> list[BotCommand]:
        return [
            BotCommand(
                command="/start",
                description=self._i18n_service.translate(key="cmd_start", lang=lang),
            ),
            BotCommand(
                command="/menu",
                description=self._i18n_service.translate(key="cmd_menu", lang=lang),
            ),
        ]
