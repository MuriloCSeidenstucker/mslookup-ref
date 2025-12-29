# pylint: disable=R0903:too-few-public-methods

import logging
import os
from enum import Enum
from logging import FileHandler

from .formatter import JsonFormatter


class LevelName(Enum):
    """Enumeração para níveis de severidade de logging.

    Define constantes que mapeiam os níveis de severidade de log de forma legível e tipada,
    permitindo configurar o logger sem depender diretamente da biblioteca padrão `logging`.
    Cada nível corresponde a um valor numérico compatível com a biblioteca `logging`, mas
    abstrai essa dependência para facilitar o uso e melhorar a clareza do código.
    """

    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


class LoggerHandler:
    """Configura e gerencia um logger para a aplicação.

    Esta classe inicializa um logger com um nível de severidade configurável, utilizando
    um formatador JSON personalizado para logs em arquivo e console. Os logs são salvos
    em um arquivo rotativo (diário, com retenção de 7 dias) no diretório 'logs' e também
    exibidos no console. Garante que o logger seja configurado apenas uma vez, evitando
    duplicação de manipuladores.

    Args:
        level (int, optional): Nível de severidade do logger, baseado em LevelName.
            Padrão é LevelName.INFO (valor: 20).

    Attributes:
        level (int): Nível de severidade configurado para o logger.
    """

    def __init__(self, level: int = LevelName.INFO):
        self.level = level.value

    def get_logger(self) -> logging.Logger:
        """Cria e configura um logger para a aplicação.

        Returns:
            logging.Logger: Instância configurada do logger 'mslookup'.

        Example:
            logger_handler = LoggerHandler(level=LevelName.DEBUG)
            logger = logger_handler.get_logger()
            logger.info("Aplicação iniciada")
            # Gera log em 'logs/mslookup.log' e no console no formato JSON.
        """

        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        file_name = "mslookup.log"
        full_file_path = os.path.join(log_dir, file_name)

        os.makedirs(log_dir, exist_ok=True)

        logger = logging.getLogger("mslookup")
        if not logger.hasHandlers():
            logger.setLevel(self.level)

            formatter = JsonFormatter()

            file_handler = FileHandler(
                full_file_path,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(self.level)

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            stream_handler.setLevel(logging.INFO)

            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)

        return logger
