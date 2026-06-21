# adapters/inbound/telegram/handlers/menu_handlers.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from adapters.inbound.telegram.features.welcome.states import WelcomeStates
from infrastructure.i18n.localization_service import LocalizationService

router = Router()


def _get_lang(message: Message) -> str:
    if message.from_user and message.from_user.language_code == "pt":
        return "pt-BR"
    return "en-US"


@router.message(Command("start"))
async def handle_start_command(
    message: Message,
    dialog_manager: DialogManager,
    localization_service: LocalizationService,
) -> None:
    lang = _get_lang(message)
    text = localization_service.translate("welcome_intro_text", lang=lang)

    await message.answer(text)
    await dialog_manager.start(
        state=WelcomeStates.start_window, mode=StartMode.RESET_STACK
    )


@router.message(Command("menu"))
async def handle_menu_command(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(
        state=WelcomeStates.start_window, mode=StartMode.RESET_STACK
    )


@router.message(Command("help"))
async def handle_help_command(
    message: Message, localization_service: LocalizationService
) -> None:
    lang = _get_lang(message)
    text = localization_service.translate("help_panel_text", lang=lang)

    await message.answer(text, parse_mode="HTML")


@router.message(Command("support"))
async def handle_support_command(
    message: Message, localization_service: LocalizationService
) -> None:
    lang = _get_lang(message)
    text = localization_service.translate("support_direct_text", lang=lang)

    await message.answer(text, parse_mode="HTML")
