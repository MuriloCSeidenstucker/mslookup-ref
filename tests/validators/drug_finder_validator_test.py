from types import SimpleNamespace

import pytest

from src.errors.types import HttpUnprocessableEntityError
from src.validators.drug_finder_validator import drug_finder_validator

# =========================
# Helpers
# =========================


def make_request(query_params: dict):
    """
    Cria um objeto request mínimo compatível com o validator.
    """
    return SimpleNamespace(query_params=query_params)


# =========================
# Caminho feliz
# =========================


def test_validator_returns_true_for_valid_request():
    request = make_request(
        {
            "name": "dipirona",
            "active_ingredient": "dipirona monoidratada",
            "registration_holder": "empresa x",
        }
    )

    result = drug_finder_validator(request)

    assert result is True


def test_validator_accepts_only_required_field():
    request = make_request(
        {
            "name": "dipirona",
        }
    )

    assert drug_finder_validator(request) is True


# =========================
# Validação do campo obrigatório
# =========================


@pytest.mark.parametrize("invalid_name", ["", None])
def test_validator_raises_error_when_name_is_invalid(invalid_name):
    request = make_request(
        {
            "name": invalid_name,
        }
    )

    with pytest.raises(HttpUnprocessableEntityError) as exc:
        drug_finder_validator(request)

    assert "name" in str(exc.value)


def test_validator_raises_error_when_name_is_missing():
    request = make_request({})

    with pytest.raises(HttpUnprocessableEntityError) as exc:
        drug_finder_validator(request)

    assert "name" in str(exc.value)


# =========================
# Validação de campos opcionais
# =========================


@pytest.mark.parametrize(
    "field,value",
    [
        ("active_ingredient", ""),
        ("registration_holder", ""),
    ],
)
def test_validator_raises_error_for_empty_optional_fields(field, value):
    request = make_request(
        {
            "name": "dipirona",
            field: value,
        }
    )

    with pytest.raises(HttpUnprocessableEntityError) as exc:
        drug_finder_validator(request)

    assert field in str(exc.value)


def test_validator_raises_error_for_invalid_field_type():
    request = make_request(
        {
            "name": 123,  # tipo inválido
        }
    )

    with pytest.raises(HttpUnprocessableEntityError) as exc:
        drug_finder_validator(request)

    assert "name" in str(exc.value)


# =========================
# Campos desconhecidos
# =========================


def test_validator_allows_unknown_fields():
    request = make_request(
        {
            "name": "dipirona",
            "unknown_field": "qualquer valor",
        }
    )

    assert drug_finder_validator(request) is True
