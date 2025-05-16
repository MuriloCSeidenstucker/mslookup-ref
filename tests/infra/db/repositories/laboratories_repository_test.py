# pylint: disable=C0116:missing-function-docstring

import pytest
from sqlalchemy import text

from mslookup_ref.domain.models.laboratories import Laboratories
from mslookup_ref.infra.db.repositories.laboratories_repository import (
    LaboratoriesRepository,
)
from mslookup_ref.infra.db.settings import connection


db_connection_handler = connection.DBConnectionHandler()
connection = db_connection_handler.get_engine().connect()

@pytest.mark.skip(reason="sensitive test")
def test_insert_laboratory():

    mocked_laboratory = Laboratories(
        full_name = "laboratory1",
        cnpj = "11111111111111",
        alt_names = ["lab1", "laborat1"],
        linked = []
    )

    laboratories_repository = LaboratoriesRepository()
    laboratory_id = laboratories_repository.insert_laboratory(mocked_laboratory)

    sql = f"""
        SELECT * FROM laboratories
        WHERE full_name = "{mocked_laboratory.full_name}"
        AND cnpj = {mocked_laboratory.cnpj}
    """
    response = connection.execute(text(sql))
    registry = response.fetchall()[0]

    assert registry.laboratory_id == laboratory_id
    assert registry.full_name == mocked_laboratory.full_name
    assert registry.cnpj == mocked_laboratory.cnpj

    connection.execute(
        text(
            f"""
        DELETE FROM laboratories WHERE laboratory_id = {registry.laboratory_id}
    """
        )
    )
    connection.commit()

@pytest.mark.skip(reason="sensitive test")
def test_select_laboratory():
    mocked_laboratory = Laboratories(
        full_name = "laboratory1",
        cnpj = "11111111111111",
        alt_names = ["lab1", "laborat1"],
        linked = []
    )

    laboratories_repository = LaboratoriesRepository()
    laboratory_id = laboratories_repository.insert_laboratory(mocked_laboratory)
    response = laboratories_repository.select_laboratory(mocked_laboratory.cnpj)

    assert response.laboratory_id == laboratory_id
    assert response.full_name == mocked_laboratory.full_name
    assert response.linked == mocked_laboratory.linked

    connection.execute(
        text(
            f"""
        DELETE FROM laboratories WHERE laboratory_id = {response.laboratory_id}
    """
        )
    )
    connection.commit()
