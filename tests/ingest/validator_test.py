from pathlib import Path
import pytest
from src.ingest.validator import validate_csv_structure, CSVValidationError

def test_validate_csv_structure_success(tmp_path: Path):
    csv_content = "NUMERO_REGISTRO_PRODUTO,NOME_PRODUTO,PRINCIPIO_ATIVO,EMPRESA_DETENTORA_REGISTRO,SITUACAO_REGISTRO,DATA_VENCIMENTO_REGISTRO,CATEGORIA_REGULATORIA\n123,Remedio,Ativo,Bio,Ativo,2025-01-01,CatA"
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    validate_csv_structure(csv_file)


def test_validate_csv_structure_missing_columns(tmp_path: Path):
    csv_content = "NUMERO_REGISTRO_PRODUTO,PRINCIPIO_ATIVO,EMPRESA_DETENTORA_REGISTRO,SITUACAO_REGISTRO,DATA_VENCIMENTO_REGISTRO,CATEGORIA_REGULATORIA\n123,Ativo,Bio,Ativo,2025-01-01,CatA"
    csv_file = tmp_path / "invalid_columns.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    with pytest.raises(CSVValidationError, match="Missing required columns: NOME_PRODUTO"):
        validate_csv_structure(csv_file)


def test_validate_csv_structure_file_not_found():
    fake_path = Path("non_existent_file.csv")

    with pytest.raises(CSVValidationError, match="CSV file does not exist"):
        validate_csv_structure(fake_path)


def test_validate_csv_structure_empty_file(tmp_path: Path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("", encoding="utf-8")

    with pytest.raises(CSVValidationError, match="CSV file is empty"):
        validate_csv_structure(csv_file)


def test_validate_csv_structure_encoding_error(tmp_path: Path):
    csv_file = tmp_path / "wrong_encoding.csv"
    csv_file.write_bytes("NOME_PRODUTO,CATEGORIA\nRemédio".encode("latin-1"))

    with pytest.raises(CSVValidationError, match="Invalid CSV encoding"):
        validate_csv_structure(csv_file)
