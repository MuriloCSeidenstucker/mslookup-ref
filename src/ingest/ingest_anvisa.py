from pathlib import Path

from src.ingest.downloader import download_anvisa_csv
from src.ingest.loader import load_csv
from src.ingest.validator import validate_csv_structure

ANVISA_CSV_URL = "https://dados.anvisa.gov.br/dados/DADOS_ABERTOS_MEDICAMENTOS.csv"


def main() -> None:
    csv_path = download_anvisa_csv(
        url=ANVISA_CSV_URL,
        destination_path=Path(r"D:\projects\mslookup-ref\raw_data\medicamentos.csv"),
    )

    validate_csv_structure(csv_path)
    load_csv(csv_path)


if __name__ == "__main__":
    main()
