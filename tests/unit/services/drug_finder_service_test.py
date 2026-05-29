import pytest
from pytest_mock import MockerFixture

from src.core.errors.domain_errors import DrugNotFoundError
from src.core.models.drugs import Drug
from src.services.drug_finder_service import DrugFinderService


def test_find_drugs_success(mocker: MockerFixture):
    mock_repository = mocker.MagicMock()

    mock_drug = Drug(
        registration_number="123456789",
        product_name="AMOXICILINA",
        product_name_normalized="amoxicilina",
        active_ingredient="AMOXICILINA",
        active_ingredient_normalized="amoxicilina",
        regulatory_category="Genérico",
        regulatory_category_normalized="generico",
        registration_holder="PRATI",
        registration_holder_normalized="prati",
        registration_status="ATIVO",
        registration_expiration_date=None,
        is_registration_valid=True,
    )
    mock_repository.find_drugs.return_value = [mock_drug]

    service = DrugFinderService(mock_repository)
    response = service.find(product_name="Amoxicilina   ")

    mock_repository.find_drugs.assert_called_once_with(
        product_name_normalized="amoxicilina",
        active_ingredient_normalized=None,
        registration_holder_normalized=None,
        regulatory_category_normalized=None,
    )
    assert response["count"] == 1
    assert response["data"][0]["product_name"] == "AMOXICILINA"
    assert response["data"][0]["registration_number"] == "123456789"


def test_find_drugs_not_found(mocker: MockerFixture):
    mock_repository = mocker.MagicMock()
    mock_repository.find_drugs.return_value = []

    service = DrugFinderService(mock_repository)
    with pytest.raises(DrugNotFoundError) as exc:
        service.find(product_name="Amoxicilina   ")

    assert "Nenhum registro ANVISA encontrado." in str(exc.value)
