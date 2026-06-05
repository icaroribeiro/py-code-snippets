import json

from adapters.out.mongodb.mappers.i18n_mapper import I18nMapper
from core.domain.i18n import I18n
from core.logging.logger_factory import get_logger
from src.adapters.out.mongodb.documents.i18n_document import I18nDocument
from src.infrastructure.config import I18nSettings
from src.infrastructure.mongodb.database import MongoDBDatabase
from src.ports.out.persistence.i18n_repository import I18nRepositoryPort

logger = get_logger(__name__)


class I18nRepository(I18nRepositoryPort):
    def __init__(self, config: I18nSettings, database_wrapper: MongoDBDatabase) -> None:
        """
        Initializes the repository extracting the native PyMongo database from the wrapper.
        """
        self._db = database_wrapper.db if database_wrapper else None
        self._config = config

    async def get_text(self, lang: str, key: str) -> str | None:
        """
        Implements the port contract to safely retrieve a string text from MongoDB.
        """
        locale_key = f"{lang}:{key}"

        try:
            if self._db is not None:
                collection = self._db[I18nDocument.Settings.name]
                doc_dict = await collection.find_one({"locale_key": locale_key})

                if doc_dict:
                    return doc_dict.get("text")
        except Exception as error:
            logger.error(
                f"Database tracking failed for i18n key '{locale_key}': {repr(error)}"
            )

        # Strategic fallback for embedded local files if the database fails or can't find
        local_text = self._load_from_local_json(lang, key)
        if local_text:
            return local_text

        return None

    async def save(self, domain_i18n: I18n) -> None:
        """
        Example of write method using the mapper to format transactional data.
        """
        if self._db is not None:
            collection = self._db[I18nDocument.Settings.name]

            # Transform the domain model into the payload that MongoDB expects
            persistence_payload = I18nMapper.to_persistence(domain_i18n)

            await collection.update_one(
                {"locale_key": domain_i18n.locale_key},
                {"$set": persistence_payload},
                upsert=True,
            )

    def _load_from_local_json(self, lang: str, key: str) -> str | None:
        """
        Helper method to safely parse the static JSON translations from the disk footprint.
        """
        file_path = self._config.path_to_files / f"{lang}.json"

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                translations = json.load(file)
                return translations.get(key)
        except (json.JSONDecodeError, IOError) as error:
            logger.error(
                f"Failed to read static localization file at {file_path}: {error}"
            )
            return None
