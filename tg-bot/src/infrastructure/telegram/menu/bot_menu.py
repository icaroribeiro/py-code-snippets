from aiogram import Bot, types

from infrastructure.cross_cutting.i18n_service import I18nService
from infrastructure.telegram.menu.translations.en_US_menu import EnUsMenu
from infrastructure.telegram.menu.translations.pt_BR_menu import PtBrMenu


class TgBotMenu:
    def __init__(self, i18n_service: I18nService) -> None:
        self._en_us_menu = EnUsMenu(i18n_service)
        self._pt_br_commands = PtBrMenu(i18n_service)

    async def register_all(self, bot: Bot) -> None:
        scope = types.BotCommandScopeAllPrivateChats()
        await bot.set_my_commands(commands=self._en_us_menu.to_list(), scope=scope)
        await bot.set_my_commands(
            commands=self._pt_br_commands.to_list(), scope=scope, language_code="pt"
        )
