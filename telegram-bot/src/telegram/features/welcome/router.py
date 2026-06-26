from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from infrastructure.config import TelegramSettings
from infrastructure.i18n import i18nService
from telegram.features.welcome.states import WelcomeStates

welcome_router = Router()


@welcome_router.startup()
async def register_welcome_pre_start_description(
    settings: TelegramSettings, bot: Bot, i18n_service: i18nService
) -> None:
    """Registers localized bot descriptions into Telegram during system startup."""
    await bot.set_my_description(
        description=i18n_service.translate(
            key="bot_pre_start_description", lang="en-US"
        )
    )

    await bot.set_my_description(
        description=i18n_service.translate(
            key="bot_pre_start_description", lang="pt-BR"
        ),
        language_code="pt",
    )


@welcome_router.message(Command("start"))
async def handle_start_command(message: Message, dialog_manager: DialogManager) -> None:
    """Triggers the interactive welcome interface dialog, resetting execution stack."""
    await dialog_manager.start(
        state=WelcomeStates.start_window, mode=StartMode.RESET_STACK
    )


@welcome_router.message(Command("menu"))
async def handle_menu_command(message: Message, dialog_manager: DialogManager) -> None:
    """Brings the user back to the main menu window."""
    await dialog_manager.start(
        state=WelcomeStates.start_window, mode=StartMode.RESET_STACK
    )


@welcome_router.message(Command("help"))
async def handle_help_command(
    message: Message,
    i18n_service: i18nService,
    user_lang: str,
) -> None:
    """Responds with static localized informational text regarding system help."""
    text = i18n_service.translate("help_panel_text", lang=user_lang)
    await message.answer(text, parse_mode="HTML")


@welcome_router.message(Command("support"))
async def handle_support_command(
    message: Message,
    i18n_service: i18nService,
    user_lang: str,
) -> None:
    """Responds with direct assistance links or instructions for human support."""
    text = i18n_service.translate("support_direct_text", lang=user_lang)
    await message.answer(text, parse_mode="HTML")
