from aiogram import types

from adapters.inbound.telegram.commands.langs.base_commands import BaseCommands


class EnCommands(BaseCommands):
    def start(self) -> types.BotCommand:
        return types.BotCommand(
            command="/start",
            description=self._i18n_service.translate("cmd_desc_start", lang="en-US"),
        )

    def hello_world(self) -> types.BotCommand:
        return types.BotCommand(
            command="/hello_world",
            description=self._i18n_service.translate(
                "cmd_desc_hello_world", lang="en-US"
            ),
        )

    def help(self) -> types.BotCommand:
        return types.BotCommand(
            command="/help",
            description=self._i18n_service.translate("cmd_desc_help", lang="en-US"),
        )

    def exit(self) -> types.BotCommand:
        return types.BotCommand(
            command="/exit",
            description=self._i18n_service.translate("cmd_desc_exit", lang="en-US"),
        )
