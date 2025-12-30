from datetime import date
from unittest.mock import Mock

import pytest

from src.data.use_cases.drug_finder import DrugFinder
from src.domain.models.drugs import Drug
from src.errors.types import HttpBadRequestError, HttpNotFoundError

# =========================
# Fixtures
# =========================


@pytest.fixture
def repository_mock():
    return Mock()


@pytest.fixture
def drug_finder(repository_mock):
    return DrugFinder(repository_mock)


@pytest.fixture
def sample_drug():
    return Drug(
        registration_number="123456",
        product_name="Dipirona",
        product_name_normalized="dipirona",
        active_ingredient="Dipirona Monoidratada",
        active_ingredient_normalized="dipirona monoidratada",
        regulatory_category="Analgésico",
        regulatory_category_normalized="analgesico",
        registration_holder="Farmacêutica X",
        registration_holder_normalized="farmaceutica x",
        registration_status="ATIVO",
        registration_expiration_date=date(2030, 12, 31),
        is_registration_valid=True,
    )


# =========================
# Validação de entrada
# =========================


@pytest.mark.parametrize("invalid_name", ["", "   ", None, 123])
def test_find_raises_bad_request_for_invalid_name(
    drug_finder,
    invalid_name,
):
    with pytest.raises(HttpBadRequestError) as exc:
        drug_finder.find(name=invalid_name)

    assert "obrigatório" in str(exc.value)


# =========================
# Comportamento do repositório
# =========================


def test_find_calls_repository_with_expected_arguments(
    drug_finder,
    repository_mock,
):
    repository_mock.find_drugs.return_value = []

    with pytest.raises(HttpNotFoundError):
        drug_finder.find(
            name="dipirona",
            active_ingredient="dipirona",
            registration_holder="empresa",
        )

    repository_mock.find_drugs.assert_called_once_with(
        product_name_normalized="dipirona",
        active_ingredient_normalized="dipirona",
        registration_holder_normalized="empresa",
        only_valid=True,
    )


def test_find_raises_not_found_when_repository_returns_empty_list(
    drug_finder,
    repository_mock,
):
    repository_mock.find_drugs.return_value = []

    with pytest.raises(HttpNotFoundError) as exc:
        drug_finder.find(name="dipirona")

    assert "Nenhum registro ANVISA encontrado" in str(exc.value)


# =========================
# Caminho feliz
# =========================


def test_find_returns_formatted_response(
    drug_finder,
    repository_mock,
    sample_drug,
):
    repository_mock.find_drugs.return_value = [sample_drug]

    result = drug_finder.find(name="dipirona")

    assert result["type"] == "DrugRegistrations"
    assert result["count"] == 1

    attributes = result["attributes"]
    assert isinstance(attributes, list)
    assert len(attributes) == 1

    item = attributes[0]

    assert item["registration_number"] == sample_drug.registration_number
    assert item["product_name"] == sample_drug.product_name
    assert item["active_ingredient"] == sample_drug.active_ingredient
    assert item["registration_holder"] == sample_drug.registration_holder
    assert item["regulatory_category"] == sample_drug.regulatory_category
    assert item["registration_status"] == sample_drug.registration_status
    assert item["expiration_date"] == "2030-12-31"


def test_find_formats_none_expiration_date(
    drug_finder,
    repository_mock,
    sample_drug,
):
    sample_drug.registration_expiration_date = None
    repository_mock.find_drugs.return_value = [sample_drug]

    result = drug_finder.find(name="dipirona")

    assert result["attributes"][0]["expiration_date"] is None
