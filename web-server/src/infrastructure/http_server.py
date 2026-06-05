from contextlib import asynccontextmanager
from typing import Awaitable, cast

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from src.adapters.inbound.http.handlers.exception_handler import HTTPExceptionHandler
from src.adapters.inbound.http.routers.root_router import root_router
from src.core.logging.logger_factory import get_logger
from src.infrastructure.container import Container

logger = get_logger(__name__)


class HTTPServer:
    def __init__(
        self, title: str = "Agile Ingestion Web Server", version: str = "1.0.0"
    ) -> None:
        self._title = title
        self._version = version
        self.container: Container | None = None
        self.app: FastAPI | None = None

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI):
        logger.info(
            "[STARTUP] Triggering declarative managed container resources initialization..."
        )
        try:
            if self.container is not None:
                await cast(Awaitable[None], self.container.init_resources())

            logger.info("[STARTUP] Infrastructure successfully warmed up.")
            yield

        except Exception as startup_error:
            logger.critical(f"[CRITICAL] Server failed to start: {startup_error}")
            raise startup_error

        finally:
            logger.info("[SHUTDOWN] Executing graceful teardown of connection pools...")
            if self.container is not None:
                await cast(Awaitable[None], self.container.shutdown_resources())
            logger.info("[SHUTDOWN] Infrastructure resources closed cleanly.")

    def _setup_exception_handlers(self, app: FastAPI) -> None:
        app.add_exception_handler(AppError, HTTPExceptionHandler.handle_app_error)
        app.add_exception_handler(
            HTTPException, HTTPExceptionHandler.handle_http_exception
        )
        app.add_exception_handler(
            RequestValidationError, HTTPExceptionHandler.handle_validation_error
        )

    def build(self) -> FastAPI:
        logger.info(
            f"Assembling FastAPI application engine instance: '{self._title}'..."
        )

        self.container = Container()
        self.container.wire(
            modules=[
                "src.adapters.in.web.dependencies.dependencies",
            ]
        )

        self.app = FastAPI(
            title=self._title, version=self._version, lifespan=self._lifespan
        )

        self.app.extra["container"] = self.container

        # Register unified routing strategy (v1, v2, etc.)
        self.app.include_router(root_router)

        # Register custom architectural exception translators
        self._setup_exception_handlers(self.app)

        logger.info("FastAPI HTTP Server stack fully assembled and structured.")
        return self.app
