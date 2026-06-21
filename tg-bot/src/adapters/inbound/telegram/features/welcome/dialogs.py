from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Format, Multi

from adapters.inbound.telegram.features.welcome.callbacks import on_click_example
from adapters.inbound.telegram.features.welcome.getters import get_welcome_data
from adapters.inbound.telegram.features.welcome.states import WelcomeStates

welcome_dialog = Dialog(
    Window(
        Multi(
            Format("{short_intro}\n"),
            Format("Olá, <b>{user_name}</b>!\n"),
            Format("{welcome_message}"),
        ),
        Row(Button(Format("Action"), id="btn_action", on_click=on_click_example)),
        state=WelcomeStates.start_window,
        getter=get_welcome_data,
        parse_mode=ParseMode.HTML,
    )
)
