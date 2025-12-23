import csv
from datetime import date, datetime
from pathlib import Path

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
    drugs: list[Drug] = []

    with csv_path.open(mode="r", encoding="latin-1", newline="") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row_number, row in enumerate(reader, start=2):
            try:
                product_name = (row.get("NOME_PRODUTO") or "").strip()
                regulatory_category = (row.get("CATEGORIA_REGULATORIA") or "").strip()
                registration_holder = (
                    row.get("EMPRESA_DETENTORA_REGISTRO") or ""
                ).strip()
                active_ingredient = row.get("PRINCIPIO_ATIVO")
                status = (row.get("SITUACAO_REGISTRO") or "").strip()

                product_name_normalized = normalize_text(product_name)
                regulatory_category_normalized = normalize_text(regulatory_category)
                registration_holder_normalized = normalize_text(registration_holder)
                active_ingredient_normalized = normalize_text(active_ingredient)

                if not product_name_normalized:
                    raise ValueError("Normalized product_name is empty")

                if not registration_holder_normalized:
                    raise ValueError("Normalized registration_holder is empty")

                if not regulatory_category_normalized:
                    logger.warning(
                        "Empty regulatory_category at row %d. Setting as 'unknown'.",
                        row_number,
                    )
                    regulatory_category = "UNKNOWN"
                    regulatory_category_normalized = "unknown"

                drug = Drug(
                    registration_number=row.get("NUMERO_REGISTRO_PRODUTO") or None,
                    product_name=product_name,
                    product_name_normalized=product_name_normalized,
                    active_ingredient=active_ingredient,
                    active_ingredient_normalized=active_ingredient_normalized,
                    regulatory_category=regulatory_category,
                    regulatory_category_normalized=regulatory_category_normalized,
                    registration_holder=registration_holder,
                    registration_holder_normalized=registration_holder_normalized,
                    registration_status=status,
                    registration_expiration_date=_parse_date(
                        row.get("DATA_VENCIMENTO_REGISTRO")
                    ),
                    is_registration_valid=status in VALID_REGISTRATION_STATUSES,
                )

                drugs.append(drug)

            except Exception:
                logger.exception("Failed to process row %d. Row skipped.", row_number)

    if not drugs:
        logger.warning("No valid drugs found to insert.")
        return

    logger.info("Inserting %d drugs into database", len(drugs))
    repository.insert_drug(drugs)
    logger.info("CSV load completed successfully")
