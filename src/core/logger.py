import logging
import sys

from pathlib import Path
from typing import Optional


class Logger:
    def __init__(self) -> None:
        self._logger = logging.getLogger("NSFWDetector")
        self._logger.setLevel(logging.DEBUG)
        self._configure_handlers()

    def _configure_handlers(self) -> None:
        formatter = logging.Formatter(
            fmt = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
            datefmt = "%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

    def setup_file_logging(
        self,
        log_file: Optional[Path] = None,
        max_bytes: int = 10 * 1024 * 1024,
        backup_count: int = 5,
    ) -> None:
        if log_file:
            log_file.parent.mkdir(parents = True, exist_ok = True)

            file_handler = logging.handlers.RotatingFileHandler(
                filename = log_file,
                maxBytes = max_bytes,
                backupCount = backup_count,
                encoding = "utf-8",
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter(
                fmt = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
                datefmt = "%Y-%m-%d %H:%M:%S",
            ))
            self._logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        return self._logger

logger = Logger().get_logger()