import inspect
from functools import lru_cache
from pathlib import Path

import orjson

from infrastructure.cross_cutting import get_logger

logger = get_logger(__name__)


class i18nService:
    """Responsible for the internationalization and localization of texts."""

    def __init__(self, default_lang: str = "en-US") -> None:
        self._default_lang = default_lang

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

    def _get_caller_i18n_path(self) -> Path:
        """Inspects the stack to find the 'i18n' directory sibling to the caller file."""
        try:
            # frame 0 is this method, frame 1 is 'translate', frame 2 is the actual caller
            frame = inspect.stack()[2]
            caller_file_path = Path(frame.filename)
            # Returns the path of the i18n folder sibling to the file that called the service
            return caller_file_path.parent / "i18n"
        except Exception as error:
            logger.error(f"Failed to inspect stack for i18n auto-detection: {error}")
            # Safe fallback if stack inspection fails in a specific runtime environment
            return Path.cwd()

    def translate(self, key: str, lang: str | None = None, **kwargs) -> str:
        locale = lang or self._default_lang

        # 1. Automatically finds the i18n directory of the calling feature
        i18n_dir = self._get_caller_i18n_path()
        target_file = i18n_dir / f"{locale}.json"

        # 2. Attempts to load the translation for the requested language
        translations = self._load_json_file(target_file)
        text = translations.get(key)

        # 3. Fallback to the default language if the key is missing in the current language
        if text is None and locale != self._default_lang:
            fallback_file = i18n_dir / f"{self._default_lang}.json"
            translations = self._load_json_file(fallback_file)
            text = translations.get(key)

        # 4. Final safety fallback if the key is missing entirely from the context
        if text is None:
            logger.warning(
                f"Translation key '{key}' missing from localized context at {i18n_dir}."
            )
            return f"[{key}]"

        return text.format(**kwargs) if kwargs else text
