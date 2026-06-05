from src.ports.out.persistence.i18n_repository import I18nRepositoryPort


class GetI18nTextUseCase:
    def __init__(self, i18n_repository: I18nRepositoryPort) -> None:
        """
        Initializes the usecase with the driven persistence port.
        """
        self._i18n_repository = i18n_repository
        self._default_fallback = "en-US"

    async def execute(self, lang: str, key: str) -> str:
        """
        Executes cascading fallback strategy across database states and file systems.
        """
        # Step 1: Strict match (e.g., Database or JSON for "es-MX")
        text = await self._i18n_repository.get_text(lang, key)
        if text:
            return text

        # Step 2: Language family match (e.g., Database or JSON for "es")
        if "-" in lang:
            base_lang = lang.split("-")[0]
            text = await self._i18n_repository.get_text(base_lang, key)
            if text:
                return text

        # Step 3: Global application fallback (Database or JSON for "en-US")
        if lang != self._default_fallback:
            text = await self._i18n_repository.get_text(self._default_fallback, key)
            if text:
                return text

        # Step 4: Emergency layout representation to avoid bot runtime failures
        return f"[{key}]"
