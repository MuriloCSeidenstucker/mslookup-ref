from pathlib import Path

from pytest_mock import MockerFixture

from src.tasks.anvisa_ingestion import PROJECT_ROOT, main


def test_anvisa_ingestion_main(mocker: MockerFixture):
    mock_setup_logging = mocker.patch("src.tasks.anvisa_ingestion.setup_logging")
    mock_downloader = mocker.patch(
        "src.tasks.anvisa_ingestion.download_anvisa_csv", return_value=Path("test.csv")
    )
    mock_validate = mocker.patch("src.tasks.anvisa_ingestion.validate_csv_structure")
    mock_loader = mocker.patch("src.tasks.anvisa_ingestion.load_csv")

    main()

    mock_setup_logging.assert_called_once()
    mock_downloader.assert_called_once_with(
        url="https://dados.anvisa.gov.br/dados/DADOS_ABERTOS_MEDICAMENTOS.csv",
        destination_path=PROJECT_ROOT / "raw_data" / "drugs.csv",
    )
    mock_validate.assert_called_once_with(Path("test.csv"))
    mock_loader.assert_called_once_with(Path("test.csv"))
