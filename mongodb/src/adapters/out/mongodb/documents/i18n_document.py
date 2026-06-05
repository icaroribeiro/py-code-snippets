from typing import Annotated

from beanie import Document, Indexed


class I18nDocument(Document):
    # locale_key ensures uniqueness and ultra-fast lookups by joining language and key (e.g., "pt-BR:welcome_msg")
    locale_key: Annotated[str, Indexed(unique=True)]
    lang: str
    key: str
    text: str

    class Settings:
        name = "i18n_dictionary"

        # Beanie automatically creates these indexes during boot (via init_beanie)
        indexes = [
            "locale_key",
            # Optional compound index in case you want to search by separate fields in the future
            [("lang", 1), ("key", 1)],
        ]
