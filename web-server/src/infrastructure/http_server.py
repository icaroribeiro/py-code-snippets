from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from adapters.inbound.http.handlers.exception_handler import HTTPExceptionHandler
from adapters.inbound.http.routers.root_router import root_router
from core.domain.errors import CoreError
from infrastructure.config import HTTPServerSettings
from infrastructure.container import Container
from infrastructure.cross_cutting.logging import get_logger

logger = get_logger(__name__)


class HTTPServer:
    def __init__(
        self,
        settings: HTTPServerSettings,
        title: str = "Agile Ingestion Web Server",
        version: str = "1.0.0",
    ) -> None:
        self._title = title
        self._version = version
        self._settings = settings

        self.container: Container | None = None
        self.app: FastAPI | None = None

    def build(self) -> FastAPI:
        try:
            logger.info(
                f"Assembling FastAPI application engine instance: '{self._title}'..."
            )

            self.container = Container()
            self.container.wire(
                modules=[
                    "adapters.inbound.http.dependencies.dependencies",
                ]
            )

            self.app = FastAPI(
                title=self._title, version=self._version, lifespan=self._lifespan
            )
            self.app.extra["container"] = self.container
            self.app.include_router(root_router)
            self._setup_exception_handlers(self.app)

            logger.info("FastAPI HTTP Server stack fully assembled and structured.")
            return self.app
        except Exception as error:
            logger.critical(f"Server failed to start: {error}")
            if self.container is not None:
                self.container.shutdown_resources()
            raise

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI):
        logger.info("FastAPI lifecycle started successfully.")
        if self.container is not None:
            self.container.init_resources()
        logger.info("Infrastructure resources initialized successfully.")
        yield
        logger.warning("Shutdown signal received. Cleaning up infrastructure...")
        if self.container is not None:
            self.container.shutdown_resources()
        logger.info("Infrastructure resources closed cleanly.")

    def _setup_exception_handlers(self, app: FastAPI) -> None:
        app.add_exception_handler(CoreError, HTTPExceptionHandler.handle_core_error)
        app.add_exception_handler(
            HTTPException, HTTPExceptionHandler.handle_http_exception
        )
        app.add_exception_handler(
            RequestValidationError, HTTPExceptionHandler.handle_validation_error
        )
