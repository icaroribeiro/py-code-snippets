import asyncio
import sys

from core.logging.logger_factory import get_logger
from src.infrastructure.container import Container

logger = get_logger(__name__)


async def start_server():
    logger.info("Starting application...")

    container = Container()

    init_resources_result = container.init_resources()
    if asyncio.iscoroutine(init_resources_result):
        await init_resources_result

    logger.info(
        "Database and migrations initialized inside the dependency container successfully."
    )

    i18n_usecase = await container.get_i18n_text_usecase.async_()

    try:
        logger.info("--- STARTING LOCALIZATION FLOW TRIALS ---")
        # Scenario A: Must fetch directly from MongoDB (Migration seed)
        txt_pt = await i18n_usecase.execute(lang="pt-BR", key="welcome_msg")
        logger.info(f"[PROMPT: pt-BR] Result from MongoDB: '{txt_pt}'")

        # Scenario B: Must fail in MongoDB and load from 'es-MX.json' file
        txt_es = await i18n_usecase.execute(lang="es-MX", key="welcome_msg")
        logger.info(f"[PROMPT: es-MX] Result from JSON File: '{txt_es}'")

        # Scenario C: Non-existent language (e.g., French), should activate the fallback chain to the global default 'en-US'
        txt_fr = await i18n_usecase.execute(lang="fr-FR", key="welcome_msg")
        logger.info(f"[PROMPT: fr-FR] Result from Global Fallback (en-US): '{txt_fr}'")

        # Scenario D: Ghost key that doesn't exist anywhere (Emergency Mode)
        txt_ghost = await i18n_usecase.execute(lang="pt-BR", key="non_existent_key")
        logger.info(f"[PROMPT: Ghost Key] Emergency Recovery Result: '{txt_ghost}'")

        logger.info("--- END OF LOCALIZATION FLOW TRIALS ---")
    except Exception as error:
        logger.error(f"Critical error during application bootstrap: {error}")
    finally:
        logger.info("Shutting down application and cleaning up resources...")
        shutdown_result = container.shutdown_resources()
        if asyncio.iscoroutine(shutdown_result):
            await shutdown_result


if __name__ == "__main__":
    asyncio.run(start_server())
    sys.exit(0)
