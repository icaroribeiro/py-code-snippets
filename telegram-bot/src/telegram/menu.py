from aiogram import Bot, types

from infrastructure.config import TelegramSettings
from infrastructure.i18n import i18nService
from telegram.features.welcome.commands.help_command import HelpCommand
from telegram.features.welcome.commands.menu_command import MenuCommand
from telegram.features.welcome.commands.start_command import StartCommand
from telegram.features.welcome.commands.support_command import SupportCommand


class TelegramMenu:
    def __init__(self, settings: TelegramSettings, i18n_service: i18nService) -> None:
        self._settings = settings
        self._i18n_service = i18n_service
        self._start_command = StartCommand(i18n_service)
        self._menu_command = MenuCommand(i18n_service)
        self._help_command = HelpCommand(i18n_service)
        self._support_command = SupportCommand(i18n_service)

    async def set_commands(self, bot: Bot) -> None:
        scope = types.BotCommandScopeAllPrivateChats()

        for lang_i18n, lang_telegram in self._settings.supported_languages:
            commands = [
                self._start_command.build(lang=lang_i18n),
                self._menu_command.build(lang=lang_i18n),
                self._help_command.build(lang=lang_i18n),
                self._support_command.build(lang=lang_i18n),
            ]

            await bot.set_my_commands(
                commands=commands, scope=scope, language_code=lang_telegram
            )
