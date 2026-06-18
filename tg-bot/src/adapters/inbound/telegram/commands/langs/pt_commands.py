from aiogram import types

from adapters.inbound.telegram.commands.langs.base_commands import BaseCommands


class PtCommands(BaseCommands):
    def start(self) -> types.BotCommand:
        return types.BotCommand(
            command="/start",
            description=self._i18n_service.translate("cmd_desc_start", lang="pt-BR"),
        )

    def hello_world(self) -> types.BotCommand:
        return types.BotCommand(
            command="/hello_world",
            description=self._i18n_service.translate(
                "cmd_desc_hello_world", lang="pt-BR"
            ),
        )

    def help(self) -> types.BotCommand:
        return types.BotCommand(
            command="/help",
            description=self._i18n_service.translate("cmd_desc_help", lang="pt-BR"),
        )

    def exit(self) -> types.BotCommand:
        return types.BotCommand(
            command="/exit",
            description=self._i18n_service.translate("cmd_desc_exit", lang="pt-BR"),
        )
