from aiogram import types

from adapters.inbound.telegram.menus.translations.base_menu import BaseMenu


class EnUsMenu(BaseMenu):
    def start(self) -> types.BotCommand:
        return types.BotCommand(
            command="/start",
            description=self._localization_service.translate("cmd_start", lang="en-US"),
        )

    def menu(self) -> types.BotCommand:
        return types.BotCommand(
            command="/menu",
            description=self._localization_service.translate("cmd_menu", lang="en-US"),
        )

    def help(self) -> types.BotCommand:
        return types.BotCommand(
            command="/help",
            description=self._localization_service.translate("cmd_help", lang="en-US"),
        )

    def support(self) -> types.BotCommand:
        return types.BotCommand(
            command="/support",
            description=self._localization_service.translate(
                "cmd_support", lang="en-US"
            ),
        )
