from dataclasses import dataclass


@dataclass(frozen=True)
class I18n:
    """
    Domain entity representing an internationalization record.
    This class is completely independent of database frameworks or delivery layers.
    The frozen=True flag ensures the domain model behaves immutably.
    """

    lang: str  # e.g., "pt-BR"
    key: str  # e.g., "welcome_msg"
    text: str  # e.g., "Olá, bem-vindo!"

    @property
    def locale_key(self) -> str:
        """
        Derives the combined locale identifier from domain properties.
        """
        return f"{self.lang}:{self.key}"
