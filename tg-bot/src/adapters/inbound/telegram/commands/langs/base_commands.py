from abc import ABC, abstractmethod

from aiogram import types

from infrastructure.cross_cutting.i18n_service import I18nService


class BaseCommands(ABC):
    def __init__(self, i18n_service: I18nService) -> None:
        self._i18n_service = i18n_service

    @abstractmethod
    def start(self) -> types.BotCommand:
        pass

    @abstractmethod
    def hello_world(self) -> types.BotCommand:
        pass

    @abstractmethod
    def help(self) -> types.BotCommand:
        pass

    @abstractmethod
    def exit(self) -> types.BotCommand:
        pass

    def to_list(self) -> list[types.BotCommand]:
        return [self.start(), self.hello_world(), self.help(), self.exit()]
