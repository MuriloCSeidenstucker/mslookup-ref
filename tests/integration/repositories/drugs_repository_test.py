import pytest
from pytest_mock import MockerFixture
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.core.models.drugs import Drug
from src.infra.db.entities.drug_entity import DrugEntity
from src.infra.db.settings.base import Base
from src.repositories.drugs_repository import DrugsRepository


@pytest.fixture(name="db_session")
def fixture_db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)


def make_drug(**kwargs):
    default_data = {
        "registration_number": "111111111",
        "product_name": "DIPIRONA",
        "product_name_normalized": "dipirona",
        "active_ingredient": "DIPIRONA SODICA",
        "active_ingredient_normalized": "dipirona sodica",
        "regulatory_category": "Novo",
        "regulatory_category_normalized": "novo",
        "registration_holder": "MEDLEY",
        "registration_holder_normalized": "medley",
        "registration_status": "ATIVO",
        "registration_expiration_date": None,
        "is_registration_valid": True,
    }
    default_data.update(kwargs)
    return Drug(**default_data)


def test_insert_drugs_success(db_session: Session):
    repository = DrugsRepository(db_session)
    drugs = [make_drug()]

    repository.insert_drugs(drugs)

    result = db_session.execute(select(DrugEntity)).scalars().all()
    assert len(result) == 1
    assert result[0].product_name == "DIPIRONA"
    assert result[0].registration_number == "111111111"


def test_find_drugs_filtering(db_session: Session):
    drugs = [
        make_drug(registration_number="111111111"),
        make_drug(registration_number="111111112", is_registration_valid=False),
        make_drug(registration_number="111111113"),
    ]
    repository = DrugsRepository(db_session)
    repository.insert_drugs(drugs)

    result = repository.find_drugs(product_name_normalized="dipirona", only_valid=True)

    assert len(result) == 2
    assert result[0].product_name == "DIPIRONA"
    assert result[0].registration_number == "111111111"


def test_insert_drugs_rollback(db_session: Session, mocker: MockerFixture):
    repository = DrugsRepository(db_session)
    mocker.patch.object(db_session, "add_all", side_effect=Exception("Database error"))

    drugs = [make_drug()]

    with pytest.raises(Exception) as exc:
        repository.insert_drugs(drugs)

    assert "Database error" in str(exc.value)
