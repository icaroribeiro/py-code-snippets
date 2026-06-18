import json
import logging
from functools import cache
from pathlib import Path

logger = logging.getLogger(__name__)


class I18nService:
    def __init__(self, default_lang: str = "en-US") -> None:
        self._default_lang = default_lang
        self._base_path = Path(__file__).resolve().parents[1] / "i18n"

    @cache
    def _load_json_file(self, lang: str) -> dict:
        file_path = self._base_path / f"{lang}.json"

        if not file_path.exists():
            logger.warning(
                f"Localization file not found for locale: '{lang}'. Falling back."
            )
            return {}

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as error:
            logger.error(
                f"Failed to read static localization file at {file_path}: {error}"
            )
            return {}

    def translate(self, key: str, lang: str | None = None, **kwargs) -> str:
        locale = lang or self._default_lang
        translations = self._load_json_file(locale)

        text = translations.get(key)
        if text is None and locale != self._default_lang:
            translations = self._load_json_file(self._default_lang)
            text = translations.get(key)

        if text is None:
            logger.warning(
                f"Translation key '{key}' missing from all localized contexts."
            )
            return f"[{key}]"

        return text.format(**kwargs) if kwargs else text
