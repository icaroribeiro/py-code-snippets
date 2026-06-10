import asyncio
import sys

from infrastructure.container import Container
from infrastructure.cross_cutting.logging import Logging, get_logger

logger = get_logger(__name__)

container = Container()


async def bootstrap_worker() -> None:
    Logging.init()
    logger.info("Starting Celery Worker application bootstrap...")
    try:
        logger.info("Initializing container stateful resources...")
        container.init_resources()
        logger.info("Celery resources and containers wired successfully.")
    except Exception as error:
        logger.error(
            f"Critical error during Celery worker bootstrap: {error}", exc_info=True
        )
        sys.exit(1)


try:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(bootstrap_worker())

    celery_broker_wrapper = container.celery_broker()

    logger.info("CeleryBroker instance retrieved successfully.")

    if celery_broker_wrapper is None:
        raise RuntimeError("Container resolved celery_broker as None")

    app = celery_broker_wrapper.app

    if app is None:
        raise RuntimeError(
            "CeleryBroker wrapper initialized, but underlying Celery app is None"
        )

    logger.info("Celery Application instance successfully exported to CLI.")
except Exception as fatal_error:
    print(
        f"CRITICAL: Failed to export Celery app to runtime CLI: {fatal_error}",
        file=sys.stderr,
    )
    sys.exit(1)

if __name__ == "__main__":
    try:
        logger.info(
            "Celery main context loaded directly. Run via 'make run-worker' to start processing."
        )
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Process context closed cleanly.")
        sys.exit(0)
