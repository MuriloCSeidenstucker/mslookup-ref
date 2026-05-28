import json
import logging
import os
import sys


class JsonFormatter(logging.Formatter):
    def format(self, record) -> str:
        datefmt = "%d-%m-%Y %H:%M:%S"
        log_data = {
            "timestamp": self.formatTime(record, datefmt),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
            "stacktrace": None,
        }
        if record.exc_info:
            log_data["stacktrace"] = self.formatException(record.exc_info)
        return json.dumps(log_data, ensure_ascii=False)


def setup_logging() -> None:
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        root_logger.addHandler(handler)

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))
