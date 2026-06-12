from celery import Celery

from infrastructure.config import CelerySettings
from infrastructure.cross_cutting.logging import Logging, get_logger

logger = get_logger(__name__)


class CeleryBroker:
    def __init__(self, broker_url: str, backend_url: str) -> None:
        self._broker_url = broker_url
        self._backend_url = backend_url
        self.app: Celery | None = None

    def init(self) -> Celery:
        Logging.init()

        logger.info("Bootstrapping Celery application lifecycle...")

        self.app = Celery(
            "agile_async_worker", broker=self._broker_url, backend=self._backend_url
        )

        if self.app is None:
            raise RuntimeError("Failed to initialize Celery application")

        self.app.config_from_object(CelerySettings)

        # Auto-discovers asynchronous tasks downstream
        self.app.autodiscover_tasks(
            packages=["src.infrastructure.celery"], related_name="tasks"
        )
        logger.info("Celery system application built successfully.")

        return self.app
