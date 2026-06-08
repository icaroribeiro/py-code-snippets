import logging
import sys
from functools import lru_cache

from pythonjsonlogger.json import JsonFormatter


class LoggerFactory:
    @staticmethod
    def init(log_level: int = logging.INFO) -> None:
        """
        Initializes the global Python root logger with a standardized JSON Formatter.
        Should be explicitly called once during the application bootstrap.
        """
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)

        while root_logger.handlers:
            root_logger.removeHandler(root_logger.handlers[0])

        handler = logging.StreamHandler(sys.stdout)

        formatter = JsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
            json_ensure_ascii=False,
        )

        handler.setFormatter(formatter)
        root_logger.addHandler(handler)

    @classmethod
    def create_logger(cls, module_name: str) -> logging.Logger:
        """
        Factory method to create or retrieve a namespaced Logger.
        """
        return logging.getLogger(module_name)


@lru_cache(maxsize=128)
def get_logger(module_name: str) -> logging.Logger:
    """
    Retrieves a cached, namespaced Logger instance for a specific module.
    """
    return LoggerFactory.create_logger(module_name)
