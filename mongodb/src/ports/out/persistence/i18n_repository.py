from abc import ABC, abstractmethod


class I18nRepositoryPort(ABC):
    @abstractmethod
    async def get_text(self, lang: str, key: str) -> str:
        pass
