from abc import ABC, abstractmethod

from aiogram import types

from infrastructure.cross_cutting.i18n_service import I18nService


class BaseMenu(ABC):
    def __init__(self, i18n_service: I18nService) -> None:
        self._i18n_service = i18n_service

    @abstractmethod
    def start(self) -> types.BotCommand:
        pass

    @abstractmethod
    def menu(self) -> types.BotCommand:
        pass

    @abstractmethod
    def help(self) -> types.BotCommand:
        pass

    @abstractmethod
    def support(self) -> types.BotCommand:
        pass

    def to_list(self) -> list[types.BotCommand]:
        return [self.start(), self.menu(), self.help(), self.support()]
