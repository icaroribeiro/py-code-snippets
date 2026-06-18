from aiogram import Bot, types

from adapters.inbound.telegram.commands.langs.en_commands import EnCommands
from adapters.inbound.telegram.commands.langs.pt_commands import PtCommands
from infrastructure.cross_cutting.i18n_service import I18nService


class BotCommands:
    def __init__(self, i18n_service: I18nService) -> None:
        self._en_commands = EnCommands(i18n_service)
        self._pt_commands = PtCommands(i18n_service)

    async def register_all(self, bot: Bot) -> None:
        scope = types.BotCommandScopeAllPrivateChats()
        await bot.set_my_commands(commands=self._en_commands.to_list(), scope=scope)
        await bot.set_my_commands(
            commands=self._pt_commands.to_list(), scope=scope, language_code="pt"
        )
