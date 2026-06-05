from celery import Celery

from src.core.logging.logger_factory import get_logger

logger = get_logger(__name__)


class CeleryMessageBroker:
    def __init__(self, broker_url: str, backend_url: str) -> None:
        self._broker_url = broker_url
        self._backend_url = backend_url
        self.app: Celery | None = None

    def init(self) -> Celery:
        logger.info("Bootstrapping Celery application lifecycle...")
        self.app = Celery(
            "agile_async_worker", broker=self._broker_url, backend=self._backend_url
        )
        if self.app is None:
            raise RuntimeError("Failed to initialize Celery application")
        self.app.conf.update(
            task_track_started=True,
            task_serializer="json",
            result_serializer="json",
            accept_content=["json"],
            enable_utc=True,
            worker_prefetch_multiplier=1,
        )
        # Auto-discovers asynchronous tasks downstream
        self.app.autodiscover_tasks(["src.infrastructure.celery.tasks"])
        logger.info("Celery system application built successfully.")
        return self.app
