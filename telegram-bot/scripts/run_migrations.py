#!/usr/bin/env python
import asyncio
import os
import sys

from beanie import init_beanie
from beanie.migrations.database import DBHandler
from beanie.migrations.models import RunningDirections, RunningMode
from beanie.migrations.runner import MigrationNode

from infrastructure.config import MongoDBSettings
from infrastructure.cross_cutting.logging import Logging, get_logger

logger = get_logger(__name__)


async def run_database_migrations() -> None:
    """
    Standalone database migration runner mapping the project's native MigrationManager logic.
    Loads settings, bootstraps Beanie, and runs migrations forward.
    """
    logger.info("Loading infrastructure configuration via Pydantic...")

    root_env_path = os.path.abspath(".env")
    mongodb_settings = MongoDBSettings(_env_file=root_env_path)  # type: ignore

    logger.info(
        f"Starting standalone MongoDB migrations targeting source path: {mongodb_settings.migrations_path}"
    )

    try:
        DBHandler.set_db(uri=mongodb_settings.uri, db_name=mongodb_settings.database)

        db_client = DBHandler.get_db()
        # Inicializa o Beanie sem modelos de documentos, pois o foco aqui são as migrações brutas
        await init_beanie(database=db_client, document_models=[])

        root_node = await MigrationNode.build(path=mongodb_settings.migrations_path)
        mode = RunningMode(direction=RunningDirections.FORWARD, distance=0)

        await root_node.run(
            mode=mode, allow_index_dropping=False, use_transaction=False
        )

        logger.info("Database migrations executed successfully.")

    except Exception as error:
        logger.critical(f"Migration runner failed unexpectedly: {repr(error)}")
        # Não chamamos sys.exit(1) aqui dentro para permitir que o bloco finalizer limpe o loop do asyncio
        raise error
    finally:
        try:
            db_client = DBHandler.get_db()
            if db_client is not None and hasattr(db_client, "client"):
                logger.info("Closing persistent MongoDB client connection pool...")
                await db_client.client.close()
        except Exception as e:
            logger.debug(f"Failed to close Mongo client smoothly: {e}")


if __name__ == "__main__":
    """Entrypoint síncrono isolando o ciclo de vida do asyncio."""
    Logging.init()

    try:
        asyncio.run(run_database_migrations())
    except Exception:
        sys.exit(1)
