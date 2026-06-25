from aiogram.fsm.state import State, StatesGroup


class WelcomeStates(StatesGroup):
    """States for the core welcome interactive dialog interface."""

    start_window = State()
