import pytest
from fastapi.testclient import TestClient

from src.infra.db.entities.drug_entity import DrugEntity
from src.main import app


@pytest.fixture(name="client")
def fixture_client():
    yield TestClient(app)


def test_get_drugs_endpoint_success(client: TestClient, db):
    db_drug = DrugEntity(
        registration_number="987654321",
        product_name="DIPIRONA",
        product_name_normalized="dipirona",
        active_ingredient="DIPIRONA SODICA",
        active_ingredient_normalized="dipirona sodica",
        regulatory_category="Novo",
        regulatory_category_normalized="novo",
        registration_holder="MEDLEY",
        registration_holder_normalized="medley",
        registration_status="ATIVO",
        registration_expiration_date=None,
        is_registration_valid=True,
    )
    db.add(db_drug)
    db.commit()

    response = client.get("/drugs/?product_name=DIPIRONA")

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["count"] == 1
    assert json_data["data"][0]["registration_number"] == "987654321"
    assert json_data["data"][0]["product_name"] == "DIPIRONA"


def test_get_drugs_endpoint_not_found(client: TestClient, db):
    # pylint: disable=unused-argument
    response = client.get("/drugs/?product_name=INEXISTENTE")

    assert response.status_code == 404
    json_data = response.json()
    assert "errors" in json_data
    assert json_data["errors"][0]["title"] == "NotFound"
    assert json_data["errors"][0]["detail"] == "Nenhum registro ANVISA encontrado."


def test_get_drugs_endpoint_validation_error(client: TestClient):
    response = client.get("/drugs/")

    assert response.status_code == 422


def test_get_drugs_endpoint_filters_invalid_drugs(client: TestClient, db):
    valid_drug = DrugEntity(
        registration_number="111111111",
        product_name="DIPIRONA",
        product_name_normalized="dipirona",
        active_ingredient="DIPIRONA SODICA",
        active_ingredient_normalized="dipirona sodica",
        regulatory_category="Novo",
        regulatory_category_normalized="novo",
        registration_holder="MEDLEY",
        registration_holder_normalized="medley",
        registration_status="ATIVO",
        registration_expiration_date=None,
        is_registration_valid=True,
    )
    invalid_drug = DrugEntity(
        registration_number="222222222",
        product_name="DIPIRONA",
        product_name_normalized="dipirona",
        active_ingredient="DIPIRONA SODICA",
        active_ingredient_normalized="dipirona sodica",
        regulatory_category="Novo",
        regulatory_category_normalized="novo",
        registration_holder="MEDLEY",
        registration_holder_normalized="medley",
        registration_status="INATIVO",
        registration_expiration_date=None,
        is_registration_valid=False,
    )
    db.add(valid_drug)
    db.add(invalid_drug)
    db.commit()

    response = client.get("/drugs/?product_name=DIPIRONA")

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["count"] == 1
    assert json_data["data"][0]["registration_number"] == "111111111"
