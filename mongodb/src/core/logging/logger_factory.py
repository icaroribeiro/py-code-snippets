import logging
import sys
from functools import lru_cache

from pythonjsonlogger.json import JsonFormatter


class LoggerFactory:
    _configured: bool = False

    @classmethod
    def create_logger(cls, module_name: str) -> logging.Logger:
        """
        Ensures the root logging subsystem is configured exactly once with a unified
        JSON output, aggressively clearing any third-party framework duplicate handlers.
        """
        if not cls._configured:
            root_logger = logging.getLogger()
            root_logger.setLevel(logging.INFO)

            # 💡 CRUCIAL: Removes any active handlers attached implicitly by Beanie,
            # Motor, or generic basicConfig configurations to stop log duplication.
            while root_logger.handlers:
                root_logger.removeHandler(root_logger.handlers[0])

            # Configures our single, authoritative JSON stream handler
            handler = logging.StreamHandler(sys.stdout)

            formatter = JsonFormatter(
                fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S%z",
                json_ensure_ascii=False,
            )

            handler.setFormatter(formatter)
            root_logger.addHandler(handler)

            cls._configured = True

        return logging.getLogger(module_name)


@lru_cache(maxsize=128)
def get_logger(module_name: str) -> logging.Logger:
    """
    Factory function leveraging an LRU cache to map and supply thread-safe,
    namespaced Logger instances efficiently across all system layers.
    """
    return LoggerFactory.create_logger(module_name)
