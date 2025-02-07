import pytest

from mslookup_ref.infra.db.repositories import MedicinesRepository


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
