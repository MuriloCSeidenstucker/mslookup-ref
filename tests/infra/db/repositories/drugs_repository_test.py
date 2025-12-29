from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from src.domain.models.drugs import Drug
from src.infra.db.repositories.drugs_repository import DrugsRepository

# =========================
# Fixtures
# =========================


@pytest.fixture
def drug():
    return Drug(
        registration_number="123",
        product_name="Produto A",
        product_name_normalized="produto a",
        active_ingredient="Ativo A",
        active_ingredient_normalized="ativo a",
        regulatory_category="Categoria",
        regulatory_category_normalized="categoria",
        registration_holder="Empresa",
        registration_holder_normalized="empresa",
        registration_status="ATIVO",
        registration_expiration_date=None,
        is_registration_valid=True,
    )


@pytest.fixture
def mock_db(mocker: MockerFixture):
    session = MagicMock()

    db = MagicMock()
    db.session = session

    db_handler = mocker.patch(
        "src.infra.db.repositories.drugs_repository.DBConnectionHandler"
    )
    db_handler.return_value.__enter__.return_value = db
    db_handler.return_value.__exit__.return_value = None

    return session


# =========================
# insert_drugs
# =========================


def test_insert_drugs_success(mock_db, drug):
    repo = DrugsRepository()

    repo.insert_drugs([drug])

    mock_db.add_all.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.rollback.assert_not_called()


def test_insert_drugs_rollback_on_exception(mock_db, drug):
    mock_db.commit.side_effect = Exception("DB error")

    repo = DrugsRepository()

    with pytest.raises(Exception):
        repo.insert_drugs([drug])

    mock_db.rollback.assert_called_once()


# =========================
# search_drugs
# =========================


def test_search_drugs_basic_query(mock_db):
    repo = DrugsRepository()

    entity = MagicMock()
    entity.registration_number = "123"
    entity.product_name = "Produto A"
    entity.product_name_normalized = "produto a"
    entity.active_ingredient = "Ativo"
    entity.active_ingredient_normalized = "ativo"
    entity.regulatory_category = "Categoria"
    entity.regulatory_category_normalized = "categoria"
    entity.registration_holder = "Empresa"
    entity.registration_holder_normalized = "empresa"
    entity.registration_status = "ATIVO"
    entity.registration_expiration_date = None
    entity.is_registration_valid = True

    mock_db.execute.return_value.scalars.return_value.all.return_value = [entity]

    results = repo.search_drugs(product_name_normalized="produto")

    assert len(results) == 1
    assert isinstance(results[0], Drug)
    assert results[0].product_name == "Produto A"


def test_search_drugs_with_optional_filters(mock_db):
    repo = DrugsRepository()

    mock_db.execute.return_value.scalars.return_value.all.return_value = []

    repo.search_drugs(
        product_name_normalized="produto",
        active_ingredient_normalized="ativo",
        registration_holder_normalized="empresa",
        only_valid=False,
        limit=10,
    )

    mock_db.execute.assert_called_once()


def test_search_drugs_only_valid_default(mock_db):
    repo = DrugsRepository()

    mock_db.execute.return_value.scalars.return_value.all.return_value = []

    repo.search_drugs(product_name_normalized="produto")

    mock_db.execute.assert_called_once()
