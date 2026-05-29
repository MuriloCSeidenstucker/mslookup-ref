# pylint: disable=W0611:unused-import

import os

import pytest
from sqlalchemy.orm import Session

from src.infra.db.entities.drug_entity import DrugEntity
from src.infra.db.settings.base import Base
from src.infra.db.settings.connection import get_engine

os.environ["DATABASE_URL"] = "sqlite:///:memory:"


@pytest.fixture(scope="session", autouse=True)
def db_setup():
    engine = get_engine()
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db():
    engine = get_engine()
    with Session(engine) as session:
        yield session
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
