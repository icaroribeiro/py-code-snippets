from aiogram import Bot, types

from infrastructure.cross_cutting import i18nService
from telegram.constants import SUPPORTED_LANGUAGES
from telegram.features.support.commands import SupportCommands
from telegram.features.welcome.commands import WelcomeCommands


class TelegramBotMenu:
    def __init__(self, i18n_service: i18nService) -> None:
        self._i18n_service = i18n_service
        self._welcome_commands = WelcomeCommands(i18n_service=i18n_service)
        self._support_commands = SupportCommands(i18n_service=i18n_service)

    async def set_commands(self, bot: Bot) -> None:
        scope = types.BotCommandScopeAllPrivateChats()

        for lang_i18n, lang_telegram in SUPPORTED_LANGUAGES:
            commands = []
            commands.extend(self._welcome_commands.get_commands(lang=lang_i18n))
            commands.extend(self._support_commands.get_commands(lang=lang_i18n))

            await bot.set_my_commands(
                commands=commands, scope=scope, language_code=lang_telegram
            )
