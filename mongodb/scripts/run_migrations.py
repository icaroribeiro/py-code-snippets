#!/usr/bin/env python
import asyncio
import os
import sys

# Ensures the root directory is in the PYTHONPATH to safely import 'src' and 'core'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from beanie import init_beanie
from beanie.migrations.database import DBHandler
from beanie.migrations.models import RunningDirections, RunningMode
from beanie.migrations.runner import MigrationNode

from src.adapters.out.mongodb.documents.i18n_document import I18nDocument
from src.core.logging.logger_factory import get_logger
from src.infrastructure.config import MongoDBSettings

logger = get_logger("migration_runner")


async def run_database_migrations():
    """
    Standalone database migration runner mapping the project's native MigrationManager logic.
    Loads settings, bootstraps Beanie, and runs migrations forward.
    """
    logger.info("Loading infrastructure configuration via Pydantic...")

    # Resolves the path to the .env file starting from the project root
    root_env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env"))
    mongodb_settings = MongoDBSettings(_env_file=root_env_path)  # type: ignore

    logger.info(
        f"Starting standalone MongoDB migrations from: {mongodb_settings.migrations_path}"
    )

    try:
        # 1. Sets up and opens the isolated connection using Beanie's native manager.
        # This eliminates the need to manually manage the Motor client here.
        DBHandler.set_db(uri=mongodb_settings.conn_string, db_name=mongodb_settings.database)

        # 2. Since init_beanie requires a database instance to map document models
        # before the migration runs (so decorators resolve schemas), we fetch the client from the DBHandler.
        db_client = DBHandler.get_db()
        await init_beanie(database=db_client, document_models=[I18nDocument])

        # 3. Rebuilds the execution node pointing to the migrations directory resolved by your .env
        root_node = await MigrationNode.build(path=mongodb_settings.migrations_path)
        mode = RunningMode(direction=RunningDirections.FORWARD, distance=0)

        # 4. Executes the migration pipeline (Up / Seeds)
        await root_node.run(
            mode=mode, allow_index_dropping=False, use_transaction=False
        )

        logger.info("Database migrations executed successfully.")

    except Exception as error:
        logger.error(f"Migration runner failed unexpectedly: {repr(error)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(run_database_migrations())
