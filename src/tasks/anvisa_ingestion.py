from pathlib import Path

from src.tasks.downloader import download_anvisa_csv
from src.tasks.loader import load_csv
from src.tasks.validator import validate_csv_structure
from src.utils.logging import setup_logging

ANVISA_CSV_URL = "https://dados.anvisa.gov.br/dados/DADOS_ABERTOS_MEDICAMENTOS.csv"
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    setup_logging()

    csv_path = download_anvisa_csv(
        url=ANVISA_CSV_URL,
        destination_path=PROJECT_ROOT / "raw_data" / "drugs.csv",
    )

    validate_csv_structure(csv_path)
    load_csv(csv_path)


if __name__ == "__main__":
    main()
