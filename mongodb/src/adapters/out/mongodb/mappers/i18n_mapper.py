from typing import Any

from src.adapters.out.mongodb.documents.i18n_document import I18nDocument
from src.core.domain.i18n import I18n


class I18nMapper:
    @staticmethod
    def to_domain(raw_entity: dict[str, Any]) -> I18n:
        """
        Transforms a raw MongoDB dictionary map into a pure, decoupled
        Core application domain entity shape.
        """
        # First validates the raw dict using the Pydantic document structure
        doc = I18nDocument.model_validate(raw_entity)

        # Maps the infrastructure document attributes to the pure immutable domain dataclass
        return I18n(lang=doc.lang, key=doc.key, text=doc.text)

    @staticmethod
    def to_persistence(domain: I18n) -> dict[str, Any]:
        """
        Transforms a pure Core application domain model into a raw dictionary
        ready to be transacted/inserted into MongoDB.
        """
        # Generates the computed locale_key required by the database index structure
        return {
            "locale_key": domain.locale_key,
            "lang": domain.lang,
            "key": domain.key,
            "text": domain.text,
        }
