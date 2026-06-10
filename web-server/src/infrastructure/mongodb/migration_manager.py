from pathlib import Path

from beanie.migrations.database import DBHandler
from beanie.migrations.models import RunningDirections, RunningMode
from beanie.migrations.runner import MigrationNode

from infrastructure.cross_cutting.logging import get_logger

logger = get_logger(__name__)


class MigrationManager:
    def __init__(
        self,
        database_uri: str,
        database_name: str,
        migrations_path: Path,
    ) -> None:
        self._database_uri = database_uri
        self._database_name = database_name
        self._path_to_migrations = migrations_path

    async def run_migrations(self) -> None:
        logger.info(f"Starting MongoDB migrations from: {self._path_to_migrations}")

        DBHandler.set_db(uri=self._database_uri, db_name=self._database_name)

        try:
            root_node = await MigrationNode.build(path=self._path_to_migrations)

            mode = RunningMode(direction=RunningDirections.FORWARD, distance=0)

            await root_node.run(
                mode=mode, allow_index_dropping=False, use_transaction=False
            )
        except Exception as error:
            logger.info(f"Error during migrations: {error}")
            raise
