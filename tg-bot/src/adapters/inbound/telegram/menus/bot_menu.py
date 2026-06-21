from aiogram import Bot, types

from adapters.inbound.telegram.menus.translations.en_US_menu import EnUsMenu
from adapters.inbound.telegram.menus.translations.pt_BR_menu import PtBrMenu
from infrastructure.i18n.localization_service import LocalizationService


class TelegramBotMenu:
    def __init__(self, localization_service: LocalizationService) -> None:
        self._localization_service = localization_service
        self._en_us_menu = EnUsMenu(localization_service)
        self._pt_br_commands = PtBrMenu(localization_service)

    async def register_all(self, bot: Bot) -> None:
        scope = types.BotCommandScopeAllPrivateChats()

        await bot.set_my_commands(commands=self._en_us_menu.to_list(), scope=scope)
        await bot.set_my_commands(
            commands=self._pt_br_commands.to_list(), scope=scope, language_code="pt"
        )

        await bot.set_my_description(
            description=self._localization_service.translate(
                "bot_pre_start_description", lang="en-US"
            )
        )
        await bot.set_my_description(
            description=self._localization_service.translate(
                "bot_pre_start_description", lang="pt-BR"
            ),
            language_code="pt",
        )
