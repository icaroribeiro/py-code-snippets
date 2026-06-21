from typing import Any

from aiogram.types import User
from aiogram_dialog import DialogManager

from infrastructure.i18n.localization_service import LocalizationService


async def get_welcome_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    event_user: User | None = dialog_manager.middleware_data.get("event_from_user")
    localization_service: LocalizationService | None = (
        dialog_manager.middleware_data.get("localization_service")
    )

    lang = "en-US"
    if event_user and event_user.language_code == "pt":
        lang = "pt-BR"

    first_name = event_user.first_name if event_user else "User"

    short_intro = ""
    welcome_text = ""

    if localization_service:
        short_intro = localization_service.translate("welcome_short_intro", lang=lang)
        welcome_text = localization_service.translate("welcome_message", lang=lang)

    return {
        "user_name": first_name,
        "short_intro": short_intro,
        "welcome_message": welcome_text,
    }
