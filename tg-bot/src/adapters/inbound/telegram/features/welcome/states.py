from aiogram.fsm.state import State, StatesGroup


class WelcomeStates(StatesGroup):
    start_window = State()
