# pylint: disable=W0212:protected-access

from contextlib import contextmanager

from sqlalchemy import text

from src.infra.db.settings.connection import get_session


def test_db_connection():
    with contextmanager(get_session)() as session:
        response = session.execute(text("SELECT 1"))
        result = response.scalar()

        assert result == 1
        assert session.is_active is True
