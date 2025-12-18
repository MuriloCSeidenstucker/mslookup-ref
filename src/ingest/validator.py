import csv
from pathlib import Path
from typing import Iterable

from src.logging.logger_handler import LevelName, LoggerHandler


logger_handler = LoggerHandler(LevelName.DEBUG)
logger = logger_handler.get_logger()


class CSVValidationError(Exception):
    """Raised when the CSV structure does not match the expected contract."""


REQUIRED_COLUMNS: set[str] = {
    "NUMERO_REGISTRO_PRODUTO",
    "NOME_PRODUTO",
    "PRINCIPIO_ATIVO",
    "EMPRESA_DETENTORA_REGISTRO",
    "SITUACAO_REGISTRO",
    "DATA_VENCIMENTO_REGISTRO",
    "CATEGORIA_REGULATORIA",
}


def validate_csv_structure(csv_path: Path) -> None:
    logger.info("Starting CSV structural validation")
    logger.info("CSV path: %s", csv_path)

    if not csv_path.exists():
        logger.error("CSV file not found")
        raise CSVValidationError("CSV file does not exist")

    try:
        with csv_path.open(mode="r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file)
            header: Iterable[str] = next(reader)
    except UnicodeDecodeError as exc:
        logger.error("Failed to decode CSV file (encoding issue)")
        raise CSVValidationError("Invalid CSV encoding") from exc
    except StopIteration as exc:
        logger.error("CSV file is empty")
        raise CSVValidationError("CSV file is empty") from exc
    except Exception as exc:
        logger.exception("Unexpected error while reading CSV header")
        raise CSVValidationError("Failed to read CSV header") from exc

    header_set = {column.strip() for column in header}

    missing_columns = REQUIRED_COLUMNS - header_set

    if missing_columns:
        logger.error("CSV structure validation failed")
        logger.error("Missing required columns: %s", missing_columns)
        raise CSVValidationError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )

    logger.info("CSV structural validation passed successfully")
