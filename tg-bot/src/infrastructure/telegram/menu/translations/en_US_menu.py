from aiogram import types

from infrastructure.telegram.menu.translations.base_menu import BaseMenu


class EnUsMenu(BaseMenu):
    def start(self) -> types.BotCommand:
        return types.BotCommand(
            command="/start",
            description=self._i18n_service.translate("cmd_start", lang="en-US"),
        )

    def menu(self) -> types.BotCommand:
        return types.BotCommand(
            command="/menu",
            description=self._i18n_service.translate("cmd_menu", lang="en-US"),
        )

    def help(self) -> types.BotCommand:
        return types.BotCommand(
            command="/help",
            description=self._i18n_service.translate("cmd_help", lang="en-US"),
        )

    def support(self) -> types.BotCommand:
        return types.BotCommand(
            command="/support",
            description=self._i18n_service.translate("cmd_support", lang="en-US"),
        )
