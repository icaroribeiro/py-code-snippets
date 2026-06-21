from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from adapters.inbound.telegram.features.welcome.states import WelcomeStates
from infrastructure.i18n.localization_service import LocalizationService

welcome_router = Router()


@welcome_router.message(Command("start"))
async def handle_start_command(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        state=WelcomeStates.start_window, mode=StartMode.RESET_STACK
    )


@welcome_router.message(Command("menu"))
async def handle_menu_command(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(
        state=WelcomeStates.start_window, mode=StartMode.RESET_STACK
    )


@welcome_router.message(Command("help"))
async def handle_help_command(
    message: Message,
    localization_service: LocalizationService,
    user_lang: str,  # <-- Injetado automaticamente pelo Middleware!
) -> None:
    text = localization_service.translate("help_panel_text", lang=user_lang)
    await message.answer(text, parse_mode="HTML")


@welcome_router.message(Command("support"))
async def handle_support_command(
    message: Message,
    localization_service: LocalizationService,
    user_lang: str,  # <-- Injetado automaticamente pelo Middleware!
) -> None:
    text = localization_service.translate("support_direct_text", lang=user_lang)
    await message.answer(text, parse_mode="HTML")
