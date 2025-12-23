import json
import logging


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
