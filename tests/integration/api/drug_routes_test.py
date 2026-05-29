import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from src.api.drug_routes import get_drug_finder_service
from src.core.errors.domain_errors import DrugNotFoundError
from src.main import app


@pytest.fixture(name="mock_service")
def fixture_mock_service(mocker: MockerFixture):
    return mocker.MagicMock()


@pytest.fixture(name="client")
def fixture_client(mock_service):
    app.dependency_overrides[get_drug_finder_service] = lambda: mock_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_get_drugs_endpoint_success(client: TestClient, mock_service):
    mock_service.find.return_value = {
        "count": 1,
        "data": [
            {
                "registration_number": "987654321",
                "product_name": "DIPIRONA",
                "active_ingredient": "DIPIRONA SODICA",
                "registration_holder": "MEDLEY",
                "regulatory_category": "Novo",
                "expiration_date": "2030-12-31",
            }
        ],
    }

    response = client.get("/drugs/?product_name=DIPIRONA")

    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["data"][0]["registration_number"] == "987654321"


def test_get_drugs_endpoint_not_found(client: TestClient, mock_service):
    mock_service.find.side_effect = DrugNotFoundError(
        "Nenhum registro ANVISA encontrado."
    )

    response = client.get("/drugs/?product_name=DIPIRONA")

    assert response.status_code == 404
    assert response.json()["errors"]
    assert response.json()["errors"][0]["title"] == "NotFound"
    assert (
        response.json()["errors"][0]["detail"] == "Nenhum registro ANVISA encontrado."
    )


def test_get_drugs_endpoint_validation_error(client: TestClient):
    response = client.get("/drugs/")

    assert response.status_code == 422
