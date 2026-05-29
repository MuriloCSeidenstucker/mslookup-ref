import csv
from pathlib import Path

import pytest

from src.tasks.validator import (
    REQUIRED_COLUMNS,
    CSVValidationError,
    validate_csv_structure,
)


def write_csv(
    path: Path,
    header: list[str] | None,
    encoding: str = "utf-8",
):
    with path.open("w", encoding=encoding, newline="") as file:
        writer = csv.writer(file, delimiter=";")
        if header is not None:
            writer.writerow(header)


def test_validate_csv_structure_file_not_found(tmp_path):
    csv_path = tmp_path / "missing.csv"

    with pytest.raises(CSVValidationError) as exc:
        validate_csv_structure(csv_path)

    assert "does not exist" in str(exc.value)


def test_validate_csv_structure_empty_file(tmp_path):
    csv_path = tmp_path / "empty.csv"
    csv_path.touch()

    with pytest.raises(CSVValidationError) as exc:
        validate_csv_structure(csv_path)

    assert "empty" in str(exc.value)


def test_validate_csv_structure_garbage_header_results_in_missing_columns(tmp_path):
    csv_path = tmp_path / "garbage.csv"
    csv_path.write_bytes(b"\xff\xfe\x00\x00")

    with pytest.raises(CSVValidationError) as exc:
        validate_csv_structure(csv_path)

    message = str(exc.value)

    assert "Missing required columns" in message
    for column in REQUIRED_COLUMNS:
        assert column in message


def test_validate_csv_structure_missing_required_columns(tmp_path):
    csv_path = tmp_path / "missing_columns.csv"

    header = [
        "NOME_PRODUTO",
        "PRINCIPIO_ATIVO",
    ]

    write_csv(csv_path, header)

    with pytest.raises(CSVValidationError) as exc:
        validate_csv_structure(csv_path)

    message = str(exc.value)
    assert "Missing required columns" in message
    for column in REQUIRED_COLUMNS - set(header):
        assert column in message


def test_validate_csv_structure_strips_header_whitespace(tmp_path):
    csv_path = tmp_path / "whitespace_header.csv"

    header = [f" {col} " for col in REQUIRED_COLUMNS]

    write_csv(csv_path, header)

    validate_csv_structure(csv_path)


def test_validate_csv_structure_latin1_encoding(tmp_path):
    csv_path = tmp_path / "latin1.csv"

    header = list(REQUIRED_COLUMNS)
    write_csv(csv_path, header, encoding="latin-1")

    validate_csv_structure(csv_path)


def test_validate_csv_structure_valid_csv(tmp_path):
    csv_path = tmp_path / "valid.csv"

    header = list(REQUIRED_COLUMNS)
    write_csv(csv_path, header)

    validate_csv_structure(csv_path)
