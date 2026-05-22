# pylint: disable=W0212:protected-access

from pytest_mock import MockerFixture
from sqlalchemy import create_engine, text

from src.infra.db.settings.connection import DBConnectionHandler


def test_db_connection_handler(mocker: MockerFixture):
    engine = create_engine("sqlite:///:memory:")

    mock_create_engine = mocker.patch("src.infra.db.settings.connection.create_engine")
    mock_create_engine.return_value = engine

    with DBConnectionHandler() as handler:
        response = handler.session.execute(text("SELECT 1"))
        result = response.scalar()

        assert result == 1
        assert handler.session.is_active is True

    assert handler.session._transaction is None
