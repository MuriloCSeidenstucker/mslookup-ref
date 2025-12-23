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

    header: Iterable[str] | None = None
    used_encoding: str | None = None

    for encoding in ("utf-8", "latin-1"):
        try:
            with csv_path.open(mode="r", encoding=encoding, newline="") as file:
                reader = csv.reader(file, delimiter=";")
                header = next(reader)
                used_encoding = encoding
                break
        except UnicodeDecodeError:
            logger.warning(
                "Failed to decode CSV using encoding '%s'. Trying next option.",
                encoding,
            )
        except StopIteration:
            logger.error("CSV file is empty")
            raise CSVValidationError("CSV file is empty")
        except Exception as exc:
            logger.exception("Unexpected error while reading CSV header")
            raise CSVValidationError("Failed to read CSV header") from exc

    if header is None:
        logger.error("Unable to decode CSV file using supported encodings")
        raise CSVValidationError("Unsupported CSV encoding")

    logger.info("CSV decoded successfully using encoding: %s", used_encoding)

    header_set = {column.strip() for column in header}

    missing_columns = REQUIRED_COLUMNS - header_set

    if missing_columns:
        logger.error("CSV structure validation failed")
        logger.error("Missing required columns: %s", missing_columns)
        raise CSVValidationError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )

    logger.info("CSV structural validation passed successfully")
