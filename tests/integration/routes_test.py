from fastapi.testclient import TestClient

from src.data.use_cases.drug_finder import DrugFinder
from src.errors.types import HttpNotFoundError
from src.main.server.server import app

client = TestClient(app, raise_server_exceptions=False)


def test_search_drugs_success(mocker):
    expected_response = {
        "type": "DrugRegistrations",
        "count": 1,
        "attributes": [
            {
                "registration_number": "123456",
                "product_name": "DIPIRONA",
                "active_ingredient": "DIPIRONA",
                "registration_holder": "EMPRESA X",
                "expiration_date": "2030-12-31",
            }
        ],
    }

    mock_find = mocker.patch.object(DrugFinder, "find", return_value=expected_response)

    response = client.get("/drugs/search?product_name=dipirona")

    assert response.status_code == 200
    assert response.json() == {"data": expected_response}
    mock_find.assert_called_once_with(
        product_name="dipirona",
        active_ingredient=None,
        registration_holder=None,
    )


def test_search_drugs_validation_error():
    response = client.get("/drugs/search")
    assert response.status_code == 422


def test_search_drugs_not_found(mocker):
    mocker.patch.object(
        DrugFinder,
        "find",
        side_effect=HttpNotFoundError("Nenhum registro ANVISA encontrado."),
    )

    response = client.get("/drugs/search?product_name=inexistente")
    assert response.status_code == 404


def test_search_drugs_internal_error(mocker):
    mocker.patch.object(
        DrugFinder,
        "find",
        side_effect=Exception("Database failure"),
    )

    response = client.get("/drugs/search?product_name=dipirona")
    assert response.status_code == 500
