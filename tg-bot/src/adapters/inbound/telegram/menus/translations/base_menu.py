from abc import ABC, abstractmethod

from aiogram import types

from infrastructure.i18n.localization_service import LocalizationService


class BaseMenu(ABC):
    def __init__(self, localization_service: LocalizationService) -> None:
        self._localization_service = localization_service

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
