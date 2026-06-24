#!/usr/bin/env python
import asyncio
import sys

from celery import Celery

from infrastructure.container import Container
from infrastructure.cross_cutting import Logging, get_logger

logger = get_logger(__name__)

# The Celery CLI expects this exact global variable name when pointing via '-A'
app: Celery | None = None


async def bootstrap_worker() -> Container:
    """Asynchronously bootstraps container dependencies and stateful resources."""
    Logging.init()
    logger.info("Starting Celery Worker application bootstrap...")
    try:
        logger.info("Initializing container stateful resources...")
        container = Container()
        container.wire(
            modules=[
                "adapters.outbound.messaging.task.tasks.create_random_number_task",
            ]
        )
        container.init_resources()
        logger.info("Celery resources and containers wired successfully.")
        return container
    except Exception as error:
        logger.error(
            f"Critical error during Celery worker bootstrap: {error}", exc_info=True
        )
        sys.exit(1)


def init_celery_worker() -> None:
    """Coordinates the worker lifecycle and exports the Celery application instance."""
    global app
    try:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Resolves the async initialization within the active loop
        container = loop.run_until_complete(bootstrap_worker())

        celery_broker_wrapper = container.celery_broker()
        logger.info("CeleryBroker instance retrieved successfully.")

        if celery_broker_wrapper is None:
            raise RuntimeError("Container resolved celery_broker as None")

        # Exports the instantiated Celery application to the global variable block
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


try:
    # Trigger execution immediately on module import so the Celery worker CLI captures the 'app' state
    init_celery_worker()
except KeyboardInterrupt:
    pass
finally:
    logger.info("Process terminated cleanly. Goodbye.")
    sys.exit(0)
