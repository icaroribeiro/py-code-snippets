from functools import lru_cache
from pathlib import Path

import orjson

from infrastructure.cross_cutting import get_logger

logger = get_logger(__name__)


class i18nService:
    """Responsible for the internationalization and localization of texts."""

    def __init__(self, default_lang: str = "en-US") -> None:
        self._default_lang = default_lang
        # Statically defines the path to the locales folder relative to this file
        self._locales_dir = Path(__file__).resolve().parent / "locales"

    @lru_cache(maxsize=128)
    def _load_json_file(self, file_path: Path) -> dict:
        """Loads and caches the translation dictionary using orjson."""
        if not file_path.exists():
            logger.warning(f"Localization file not found at: '{file_path}'.")
            return {}

        try:
            # orjson reads bytes directly, which delivers maximum performance
            binary_data = file_path.read_bytes()
            if not binary_data:
                return {}
            return orjson.loads(binary_data)
        except (orjson.JSONDecodeError, IOError) as error:
            logger.error(f"Failed to read localization file at {file_path}: {error}")
            return {}

    def translate(self, key: str, lang: str | None = None, **kwargs) -> str:
        locale = lang or self._default_lang

        # 1. Targets the specific locale file within the centralized infrastructure directory
        target_file = self._locales_dir / f"{locale}.json"

        # 2. Attempts to load the translation for the requested language
        translations = self._load_json_file(target_file)
        text = translations.get(key)

        # 3. Fallback to the default language if the key is missing in the current language
        if text is None and locale != self._default_lang:
            fallback_file = self._locales_dir / f"{self._default_lang}.json"
            translations = self._load_json_file(fallback_file)
            text = translations.get(key)

        # 4. Final safety fallback if the key is missing entirely from the context
        if text is None:
            logger.warning(
                f"Translation key '{key}' missing from localized context at {self._locales_dir}."
            )
            return f"[{key}]"

        return text.format(**kwargs) if kwargs else text
