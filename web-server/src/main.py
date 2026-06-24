import asyncio
import sys

import uvicorn
from fastapi import FastAPI

from infrastructure.config import get_http_server_settings
from infrastructure.cross_cutting import Logging, get_logger
from infrastructure.http_server import HTTPServer

logger = get_logger(__name__)

Logging.init()


def create_app() -> FastAPI:
    """
    Application Factory for Uvicorn CLI.
    This function is executed by Uvicorn's workers safely.
    """
    try:
        logger.info("Loading server configuration...")
        http_server_settings = get_http_server_settings()

        logger.info(
            f"Server configured for environment: {http_server_settings.env.upper()} "
            f"(http://{http_server_settings.host}:{http_server_settings.port})"
        )

        http_server = HTTPServer(
            settings=http_server_settings, title="Default Web Server", version="1.0.0"
        )

        logger.info("Building FastAPI application...")
        return http_server.build()
    except Exception as error:
        logger.critical(
            f"Failed to initialize server module via factory: {repr(error)}"
        )
        sys.exit(1)


app = create_app()


async def init_http_server() -> None:
    """Initializes and runs the FastAPI application server via Uvicorn within the active loop."""
    logger.info("Starting HTTP server supervisor...")
    try:
        http_server_settings = get_http_server_settings()
        config = uvicorn.Config(
            app=app,
            host=http_server_settings.host,
            port=http_server_settings.port,
            log_level="info",
            reload=False,
        )
        server = uvicorn.Server(config)
        logger.info("Uvicorn engine started. Server is running.")
        await server.serve()
    except (
        KeyboardInterrupt,
        asyncio.CancelledError,
    ):
        logger.warning("Shutdown signal received. Stopping server gracefully...")
    except Exception as error:
        logger.error(f"Server crashed during runtime execution: {repr(error)}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(init_http_server())
    except KeyboardInterrupt, asyncio.CancelledError:
        pass
    finally:
        logger.info("Process terminated cleanly. Goodbye.")
        sys.exit(0)
