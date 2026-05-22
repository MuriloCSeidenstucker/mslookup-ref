import runpy

import pytest
from pytest_mock import MockerFixture
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError

from src.infra.db.settings.create_tables import create_tables


def test_create_tables_success(mocker: MockerFixture):
    engine = create_engine("sqlite:///:memory:")

    mock_create_engine = mocker.patch("src.infra.db.settings.connection.create_engine")
    mock_create_engine.return_value = engine

    create_tables()

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "drugs" in tables


def test_create_tables_failure(mocker: MockerFixture):
    engine = create_engine("sqlite:///:memory:")

    mock_create_engine = mocker.patch("src.infra.db.settings.connection.create_engine")
    mock_create_engine.return_value = engine
    mock_create_all = mocker.patch(
        "src.infra.db.settings.create_tables.Base.metadata.create_all"
    )
    mock_create_all.side_effect = SQLAlchemyError("Erro simulado no banco")

    with pytest.raises(SQLAlchemyError):
        create_tables()


def test_create_tables_main(mocker: MockerFixture):
    mock_connection = mocker.patch(
        "src.infra.db.settings.connection.DBConnectionHandler"
    )
    mock_create_all = mocker.patch(
        "src.infra.db.settings.base.Base.metadata.create_all"
    )

    runpy.run_module("src.infra.db.settings.create_tables", run_name="__main__")

    mock_connection.assert_called_once()
    mock_create_all.assert_called_once()
