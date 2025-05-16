import json
import logging

from flask import g


class JsonFormatter(logging.Formatter):
    """Formatador personalizado para logs em formato JSON.

    Esta classe estende logging.Formatter para gerar logs estruturados em formato JSON,
    incluindo informações como timestamp, nível de severidade, módulo, mensagem, e
    rastreamento de pilha (stacktrace) quando aplicável. Utiliza o objeto `g` do Flask
    para incluir um identificador de log (`log_id`), se disponível, facilitando a
    rastreabilidade em aplicações web.
    """

    def format(self, record) -> str:
        """Converte um registro de log em uma string JSON.

        Args:
            record (logging.LogRecord): Registro de log a ser formatado.

        Returns:
            str: String JSON contendo os dados do log estruturados.
        """

        datefmt = "%d-%m-%Y %H:%M:%S"
        log_data = {
            "timestamp": self.formatTime(record, datefmt),
            "log_id": getattr(g, "log_id", "no_id"),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
            "stacktrace": None,
        }

        if record.exc_info:
            log_data["stacktrace"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)
