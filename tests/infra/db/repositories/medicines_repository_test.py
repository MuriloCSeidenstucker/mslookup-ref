import pytest
from sqlalchemy import text

from mslookup_ref.infra.db.repositories import MedicinesRepository
from mslookup_ref.infra.db.settings.connection import DBConnectionHandler

db_connection_handler = DBConnectionHandler()
connection = db_connection_handler.get_engine().connect()


@pytest.mark.skip(reason="sensitive test")
def test_insert_medicine():
    """Teste para verificar a inserção de um novo medicamento no banco de dados.

    Skipped:
        Este teste está sendo ignorado devido a questões sensíveis relacionadas ao banco de dados.
    """
    mocked_medicine = {
        "id": 1134301010036,
        "product": "PARACETAMOL",
        "substance": "PARACETAMOL",
        "presentation": "500 MG COM BL AL PLAS AMB X 500",
        "product_type": "Genérico",
        "ean": 7898123905141,
        "cnpj": 19570720000110,
        "laboratorie": "HIPOLABOR FARMACEUTICA LTDA",
    }

    medicines_repository = MedicinesRepository()
    medicines_repository.insert_medicine(**mocked_medicine)

    sql = f"""
        SELECT * FROM medicines
        WHERE product = '{mocked_medicine["product"]}'
        AND cnpj = {mocked_medicine["cnpj"]}
    """
    response = connection.execute(text(sql))
    registry = response.fetchall()[0]

    assert registry.product == mocked_medicine["product"]
    assert registry.cnpj == mocked_medicine["cnpj"]

    connection.execute(
        text(
            f"""
        DELETE FROM medicines WHERE id = {registry.id}
    """
        )
    )
    connection.commit()
