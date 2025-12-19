import pytest
from pathlib import Path
from datetime import date
from src.ingest.loader import load_csv, _parse_date

@pytest.mark.parametrize("input_date, expected", [
    ("25/12/2024", date(2024, 12, 25)),
    ("01/01/1899", None),
    ("01/01/2101", None),
    ("data-invalida", None),
    ("", None),
    (None, None),
])
def test_parse_date_logic(input_date, expected):
    assert _parse_date(input_date) == expected


def test_load_csv_success(mocker, tmp_path):
    mock_repo_class = mocker.patch("src.ingest.loader.DrugsRepository")
    mock_repo_instance = mock_repo_class.return_value

    csv_file = tmp_path / "test_drugs.csv"
    content = (
        "NUMERO_REGISTRO_PRODUTO,NOME_PRODUTO,PRINCIPIO_ATIVO,CATEGORIA_REGULATORIA,"
        "EMPRESA_DETENTORA_REGISTRO,SITUACAO_REGISTRO,DATA_VENCIMENTO_REGISTRO\n"
        "12345,Remedio A,Ativo X,Generico,Empresa A,ATIVO,10/10/2025\n"
        "67890,Remedio B,Ativo Y,Similar,Empresa B,VÁLIDO,15/05/2030"
    )
    csv_file.write_text(content, encoding="utf-8")

    load_csv(csv_file)

    assert mock_repo_instance.insert_drug.call_count == 2

    first_call_drug = mock_repo_instance.insert_drug.call_args_list[0][0][0]
    assert first_call_drug.product_name == "Remedio A"
    assert first_call_drug.is_registration_valid is True
    assert first_call_drug.registration_expiration_date == date(2025, 10, 10)


def test_load_csv_with_invalid_row_skips_and_continues(mocker, tmp_path):
    mock_repo = mocker.patch("src.ingest.loader.DrugsRepository").return_value
    mock_logger = mocker.patch("src.ingest.loader.logger")

    csv_file = tmp_path / "corrupt.csv"
    content = (
        "NUMERO_REGISTRO_PRODUTO,NOME_PRODUTO,PRINCIPIO_ATIVO,CATEGORIA_REGULATORIA,"
        "EMPRESA_DETENTORA_REGISTRO,SITUACAO_REGISTRO,DATA_VENCIMENTO_REGISTRO\n"
        "1,Certo,,Cat,Emp,ATIVO,01/01/2025\n"
        "2,ERRO_AQUI,,Cat" # Linha mal formada que causará KeyError no row["EMPRESA..."]
    )
    csv_file.write_text(content, encoding="utf-8")

    load_csv(csv_file)

    assert mock_repo.insert_drug.call_count == 1
    mock_logger.exception.assert_called()


def test_load_csv_registration_validity(mocker, tmp_path):
    mock_repo = mocker.patch("src.ingest.loader.DrugsRepository").return_value

    csv_file = tmp_path / "status_test.csv"
    content = (
        "NUMERO_REGISTRO_PRODUTO,NOME_PRODUTO,PRINCIPIO_ATIVO,CATEGORIA_REGULATORIA,"
        "EMPRESA_DETENTORA_REGISTRO,SITUACAO_REGISTRO,DATA_VENCIMENTO_REGISTRO\n"
        "1,Ativo,X,C,E,ATIVO,01/01/2025\n"
        "2,Inativo,X,C,E,CANCELADO,01/01/2025"
    )
    csv_file.write_text(content, encoding="utf-8")

    load_csv(csv_file)

    drugs = [call[0][0] for call in mock_repo.insert_drug.call_args_list]

    assert drugs[0].is_registration_valid is True
    assert drugs[1].is_registration_valid is False
