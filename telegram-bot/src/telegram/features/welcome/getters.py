# from typing import Any

# from aiogram.types import User
# from aiogram_dialog import DialogManager

# from infrastructure.cross_cutting import i18nService


# async def get_welcome_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
#     event_user: User | None = dialog_manager.middleware_data.get("event_from_user")
#     i18n_service: i18nService | None = dialog_manager.middleware_data.get(
#         "i18n_service"
#     )

#     lang = "en-US"
#     if event_user and event_user.language_code == "pt":
#         lang = "pt-BR"

#     first_name = event_user.first_name if event_user else "User"

#     short_intro = ""
#     welcome_text = ""

#     if i18n_service:
#         short_intro = i18n_service.translate("welcome_short_intro", lang=lang)
#         welcome_text = i18n_service.translate("welcome_message", lang=lang)

#     return {
#         "user_name": first_name,
#         "short_intro": short_intro,
#         "welcome_message": welcome_text,
#     }
