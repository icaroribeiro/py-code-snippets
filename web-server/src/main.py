import asyncio
import sys

import uvicorn

from infrastructure.config import get_http_server_settings
from infrastructure.http_server import HTTPServer
from infrastructure.logging import LoggerFactory, get_logger

logger = get_logger(__name__)


http_server_settings = get_http_server_settings()

logger.info(
    f"Starting {http_server_settings.env.upper()} server on http://{http_server_settings.host}:{http_server_settings.port}"
)

http_server_builder = HTTPServer(
    settings=http_server_settings, title="Default Web Server", version="1.0.0"
)

app = http_server_builder.build()


async def start_server():
    LoggerFactory.init()

    logger.info("Starting application bootstrap...")
    try:
        config = uvicorn.Config(
            app=app,
            host=http_server_settings.host,
            port=http_server_settings.port,
            log_level="info",
            reload=False,
        )

        server = uvicorn.Server(config)
        await server.serve()
    except KeyboardInterrupt, asyncio.CancelledError:
        logger.info("Server loop execution intercepted and cancelled successfully.")
    except Exception as error:
        logger.error(f"Critical error during application bootstrap: {error}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt, asyncio.CancelledError:
        pass
    finally:
        logger.info("Process terminated cleanly. Goodbye.")
        sys.exit(0)
