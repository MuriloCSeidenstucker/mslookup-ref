import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


def get_logger(name: str) -> logging.Logger:
    """Cria e configura um logger com base no nome fornecido."""

    date = datetime.now().strftime("%d-%m-%Y")
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    file_name = f"{date}_mslookup.log"
    full_file_path = os.path.join(log_dir, file_name)

    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(name)s - [%(filename)s:%(lineno)d] - %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
        )

        file_handler = TimedRotatingFileHandler(
            full_file_path, when="midnight", interval=1, backupCount=7, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.INFO)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
