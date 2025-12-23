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
    csv_path = tmp_path / "test.csv"
    with csv_path.open("w", encoding="latin-1", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=rows[0].keys(),
            delimiter=";",
        )
        writer.writeheader()
        writer.writerows(rows)
    return csv_path


# =========================
# _parse_date
# =========================


@pytest.mark.parametrize(
    "value,expected",
    [
        ("01/01/2020", date(2020, 1, 1)),
        ("31/12/1900", date(1900, 12, 31)),
        ("31/12/2100", date(2100, 12, 31)),
    ],
)
def test_parse_date_valid(value, expected):
    assert module._parse_date(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        None,
        "",
        "invalid",
        "01-01-2020",
        "01/01/1800",  # abaixo do range
        "01/01/2200",  # acima do range
    ],
)
def test_parse_date_invalid_returns_none(value):
    assert module._parse_date(value) is None


# =========================
# load_csv
# =========================


def test_load_csv_happy_path(mocker, tmp_path):
    # Arrange
    normalize_mock = mocker.patch(
        "src.ingest.loader.normalize_text",
        side_effect=lambda x: x.lower() if x else None,
    )

    drug_cls = mocker.patch("src.ingest.loader.Drug")
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
            "DATA_VENCIMENTO_REGISTRO": "01/01/2030",
        }
    ]

    csv_path = create_csv(tmp_path, rows)

    # Act
    module.load_csv(csv_path)

    # Assert
    repo_instance.insert_drug.assert_called_once()
    drugs_passed = repo_instance.insert_drug.call_args.args[0]

    assert len(drugs_passed) == 1
    drug_cls.assert_called_once()
    normalize_mock.assert_any_call("Produto A")


def test_load_csv_empty_file_logs_warning_and_does_not_insert(mocker, tmp_path):
    # Arrange
    mocker.patch("src.ingest.loader.normalize_text", return_value=None)
    repo_cls = mocker.patch("src.ingest.loader.DrugsRepository")
    logger = mocker.patch("src.ingest.loader.logger")

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
    repo_cls.return_value.insert_drug.assert_not_called()
    logger.warning.assert_any_call("No valid drugs found to insert.")


def test_load_csv_invalid_row_is_skipped_and_logged(mocker, tmp_path):
    # Arrange
    mocker.patch(
        "src.ingest.loader.normalize_text",
        side_effect=lambda x: "" if x == "INVALID" else x,
    )

    logger = mocker.patch("src.ingest.loader.logger")
    repo_cls = mocker.patch("src.ingest.loader.DrugsRepository")

    rows = [
        {
            "NUMERO_REGISTRO_PRODUTO": "1",
            "NOME_PRODUTO": "INVALID",
            "PRINCIPIO_ATIVO": "Ativo",
            "CATEGORIA_REGULATORIA": "Categoria",
            "EMPRESA_DETENTORA_REGISTRO": "Empresa",
            "SITUACAO_REGISTRO": "ATIVO",
            "DATA_VENCIMENTO_REGISTRO": "01/01/2030",
        }
    ]

    csv_path = create_csv(tmp_path, rows)

    # Act
    module.load_csv(csv_path)

    # Assert
    logger.exception.assert_called()
    repo_cls.return_value.insert_drug.assert_not_called()


def test_load_csv_sets_unknown_regulatory_category(mocker, tmp_path):
    # Arrange
    mocker.patch(
        "src.ingest.loader.normalize_text",
        side_effect=lambda x: "" if x == "EMPTY" else x.lower(),
    )

    drug_cls = mocker.patch("src.ingest.loader.Drug")
    repo_cls = mocker.patch("src.ingest.loader.DrugsRepository")

    rows = [
        {
            "NUMERO_REGISTRO_PRODUTO": "1",
            "NOME_PRODUTO": "Produto",
            "PRINCIPIO_ATIVO": "Ativo",
            "CATEGORIA_REGULATORIA": "EMPTY",
            "EMPRESA_DETENTORA_REGISTRO": "Empresa",
            "SITUACAO_REGISTRO": "ATIVO",
            "DATA_VENCIMENTO_REGISTRO": "01/01/2030",
        }
    ]

    csv_path = create_csv(tmp_path, rows)

    # Act
    module.load_csv(csv_path)

    # Assert
    kwargs = drug_cls.call_args.kwargs
    assert kwargs["regulatory_category"] == "UNKNOWN"
    assert kwargs["regulatory_category_normalized"] == "unknown"
