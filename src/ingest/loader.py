import csv
from pathlib import Path
from datetime import datetime, date

from src.domain.models.drugs import Drug
from src.infra.db.repositories.drugs_repository import DrugsRepository
from src.ingest.normalizer import normalize_text
from src.logging.logger_handler import LevelName, LoggerHandler


logger_handler = LoggerHandler(LevelName.DEBUG)
logger = logger_handler.get_logger()

DATE_FORMAT = "%d/%m/%Y"
MIN_YEAR = 1900
MAX_YEAR = 2100

VALID_REGISTRATION_STATUSES = {"ATIVO", "VÁLIDO"}


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None

    try:
        parsed = datetime.strptime(value, DATE_FORMAT).date()
    except ValueError:
        return None

    if not MIN_YEAR <= parsed.year <= MAX_YEAR:
        return None

    return parsed


def load_csv(csv_path: Path) -> None:
    logger.info("Starting CSV load")

    repository = DrugsRepository()

    with csv_path.open(mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=2):
            try:
                status = row.get("SITUACAO_REGISTRO", "").strip()

                drug = Drug(
                    registration_number=row.get("NUMERO_REGISTRO_PRODUTO") or None,
                    product_name=row["NOME_PRODUTO"].strip(),
                    active_ingredient=row.get("PRINCIPIO_ATIVO"),
                    regulatory_category=row["CATEGORIA_REGULATORIA"].strip(),
                    registration_holder=row["EMPRESA_DETENTORA_REGISTRO"].strip(),
                    registration_status=status,
                    registration_expiration_date=_parse_date(
                        row.get("DATA_VENCIMENTO_REGISTRO")
                    ),
                    is_registration_valid=status in VALID_REGISTRATION_STATUSES,
                )

                repository.insert_drug(drug)

            except Exception:
                logger.exception(
                    "Failed to process row %d. Row skipped.", row_number
                )
