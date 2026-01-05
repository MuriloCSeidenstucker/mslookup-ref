# pylint: disable=W0212:protected-access

import csv
from datetime import date
from pathlib import Path

import pytest

import src.ingest.loader as module

# =========================
# Helpers
# =========================


def create_csv(tmp_path: Path, rows: list[dict]) -> Path:
    path = tmp_path / "test.csv"
    with path.open("w", encoding="latin-1", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=rows[0].keys(),
            delimiter=";",
        )
        writer.writeheader()
        writer.writerows(rows)
    return path


# =========================
# _parse_date
# =========================


@pytest.mark.parametrize(
    "value,expected",
    [
        ("01/01/2025", date(2025, 1, 1)),
        ("31/12/1900", date(1900, 12, 31)),
        ("31/12/2100", date(2100, 12, 31)),
    ],
)
def test_parse_date_valid(value, expected):
    assert module._parse_date(value) == expected


@pytest.mark.parametrize(
    "value",
    ["", None, "invalid", "01-01-2025", "01/01/1800", "01/01/2200"],
)
def test_parse_date_invalid_returns_none(value):
    assert module._parse_date(value) is None


# =========================
# _is_valid_by_expiration
# =========================


def test_is_valid_by_expiration_none():
    assert module._is_valid_by_expiration(None) is False


def test_is_valid_by_expiration_future_date(mocker):
    mocker.patch.object(module, "date", wraps=date)
    module.date.today = lambda: date(2024, 1, 1)

    assert module._is_valid_by_expiration(date(2025, 1, 1)) is True


def test_is_valid_by_expiration_past_date(mocker):
    mocker.patch.object(module, "date", wraps=date)
    module.date.today = lambda: date(2024, 1, 1)

    assert module._is_valid_by_expiration(date(2023, 12, 31)) is False


# =========================
# load_csv
# =========================


def test_load_csv_happy_path(mocker, tmp_path):
    # Arrange
    mocker.patch(
        "src.ingest.loader.normalize_text",
        side_effect=lambda x: x.lower() if x else None,
    )

    repo_cls = mocker.patch("src.ingest.loader.DrugsRepository")
    repo_instance = repo_cls.return_value

    rows = [
        {
            "NUMERO_REGISTRO_PRODUTO": "123",
            "NOME_PRODUTO": "Produto A",
            "PRINCIPIO_ATIVO": "Ativo A",
            "CATEGORIA_REGULATORIA": "Categoria",
            "EMPRESA_DETENTORA_REGISTRO": "Empresa",
            "SITUACAO_REGISTRO": "ATIVO",
            "DATA_VENCIMENTO_REGISTRO": "01/01/2099",
        }
    ]

    csv_path = create_csv(tmp_path, rows)

    # Act
    module.load_csv(csv_path)

    # Assert
    repo_instance.insert_drugs.assert_called_once()
    drugs = repo_instance.insert_drugs.call_args.args[0]

    assert len(drugs) == 1
    assert drugs[0].is_registration_valid is True


def test_load_csv_sets_unknown_regulatory_category(mocker, tmp_path):
    # Arrange
    mocker.patch(
        "src.ingest.loader.normalize_text",
        side_effect=lambda x: "" if x == "EMPTY" else x.lower(),
    )

    repo_cls = mocker.patch("src.ingest.loader.DrugsRepository")

    rows = [
        {
            "NUMERO_REGISTRO_PRODUTO": "1",
            "NOME_PRODUTO": "Produto",
            "PRINCIPIO_ATIVO": "Ativo",
            "CATEGORIA_REGULATORIA": "EMPTY",
            "EMPRESA_DETENTORA_REGISTRO": "Empresa",
            "SITUACAO_REGISTRO": "ATIVO",
            "DATA_VENCIMENTO_REGISTRO": "01/01/2099",
        }
    ]

    csv_path = create_csv(tmp_path, rows)

    # Act
    module.load_csv(csv_path)

    # Assert
    drug = repo_cls.return_value.insert_drugs.call_args.args[0][0]
    assert drug.regulatory_category == "UNKNOWN"
    assert drug.regulatory_category_normalized == "unknown"


def test_load_csv_invalid_row_is_skipped(mocker, tmp_path):
    # Arrange
    mocker.patch(
        "src.ingest.loader.normalize_text",
        return_value=None,  # força falha de validação
    )

    repo_cls = mocker.patch("src.ingest.loader.DrugsRepository")

    rows = [
        {
            "NUMERO_REGISTRO_PRODUTO": "1",
            "NOME_PRODUTO": "Produto",
            "PRINCIPIO_ATIVO": "Ativo",
            "CATEGORIA_REGULATORIA": "Categoria",
            "EMPRESA_DETENTORA_REGISTRO": "Empresa",
            "SITUACAO_REGISTRO": "ATIVO",
            "DATA_VENCIMENTO_REGISTRO": "01/01/2099",
        }
    ]

    csv_path = create_csv(tmp_path, rows)

    # Act
    module.load_csv(csv_path)

    # Assert
    repo_cls.return_value.insert_drugs.assert_not_called()


def test_load_csv_no_valid_rows_does_not_insert(mocker, tmp_path):
    # Arrange
    mocker.patch("src.ingest.loader.normalize_text", return_value=None)
    repo_cls = mocker.patch("src.ingest.loader.DrugsRepository")

    rows = [
        {
            "NUMERO_REGISTRO_PRODUTO": "",
            "NOME_PRODUTO": "",
            "PRINCIPIO_ATIVO": "",
            "CATEGORIA_REGULATORIA": "",
            "EMPRESA_DETENTORA_REGISTRO": "",
            "SITUACAO_REGISTRO": "",
            "DATA_VENCIMENTO_REGISTRO": "",
        }
    ]

    csv_path = create_csv(tmp_path, rows)

    # Act
    module.load_csv(csv_path)

    # Assert
    repo_cls.return_value.insert_drugs.assert_not_called()
