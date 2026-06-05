import logging
import sys
from functools import lru_cache

from pythonjsonlogger.json import JsonFormatter


class LoggerFactory:
    _CONFIGURED: bool = False

    @classmethod
    def create_logger(cls, module_name: str) -> logging.Logger:
        if not cls._CONFIGURED:
            root_logger = logging.getLogger()
            root_logger.setLevel(logging.INFO)

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

            cls._CONFIGURED = True

        return logging.getLogger(module_name)


@lru_cache(maxsize=128)
def get_logger(module_name: str) -> logging.Logger:
    return LoggerFactory.create_logger(module_name)
