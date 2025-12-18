import pytest
from sqlalchemy import text

from src.domain.models.medicines import Medicines
from src.infra.db.repositories import MedicinesRepository
from src.infra.db.settings.connection import DBConnectionHandler

db_connection_handler = DBConnectionHandler()
connection = db_connection_handler.get_engine().connect()


@pytest.mark.skip(reason="sensitive test")
def test_insert_medicine():
    """
    Testa a inserção de um novo medicamento no banco de dados via MedicinesRepository.

    Verifica se o método insert_medicine insere corretamente os dados de um medicamento
    no banco de dados e se os valores inseridos podem ser recuperados conforme esperado.

    Args:
        Nenhum argumento é recebido diretamente, mas o teste utiliza:
            - connection: Objeto de conexão com o banco de dados (assumido importado).
            - text: Função para criar objetos de texto SQL (assumida importada).

    Raises:
        AssertionError: Se os valores inseridos não corresponderem aos mockados.
        sqlalchemy.exc.SQLAlchemyError: Possível falha na execução das queries SQL.
        IndexError: Se nenhum registro for encontrado na consulta.

    Examples:
        Execute o teste com:
            task test

    Note:
        - Teste marcado como skip devido a dados sensíveis (@pytest.mark.skip).
        - Requer conexão ativa com banco de dados.
        - Assume a existência da tabela 'medicines' e da classe MedicinesRepository.
        - Realiza limpeza dos dados inseridos após a execução.
    """
    mocked_medicine = Medicines(
        medicine_id=1111111111111,
        product="product1",
        substance="substance1;substance2;substance3",
        presentation="presentation1",
        product_type="product_type1",
        ean=1111111111111,
        cnpj=11111111111111,
        laboratory="laboratory1",
    )

    medicines_repository = MedicinesRepository()
    medicines_repository.insert_medicine(mocked_medicine)

    sql = f"""
        SELECT * FROM medicines
        WHERE product = '{mocked_medicine.product}'
        AND cnpj = {mocked_medicine.cnpj}
    """
    response = connection.execute(text(sql))
    registry = response.fetchall()[0]

    assert registry.medicine_id == mocked_medicine.medicine_id
    assert registry.product == mocked_medicine.product
    assert registry.cnpj == mocked_medicine.cnpj

    connection.execute(
        text(
            f"""
        DELETE FROM medicines WHERE medicine_id = {registry.medicine_id}
    """
        )
    )
    connection.commit()


@pytest.mark.skip(reason="sensitive test")
def test_select_medicine():
    """Testa a funcionalidade de seleção de medicamentos no MedicinesRepository.

    Este teste verifica a inserção e recuperação correta de dados de medicamentos,
    garantindo que o MedicinesRepository retorne os valores esperados.

    Args:
        Nenhum argumento é recebido diretamente, mas o teste utiliza:
            - connection: Objeto de conexão com o banco de dados (assumido importado)
            - text: Função para criar objetos de texto SQL (assumida importada)

    Raises:
        AssertionError: Se os valores retornados não corresponderem aos mockados.
        sqlalchemy.exc.SQLAlchemyError: Possível se houver falha na execução SQL.

    Examples:
        Este é um teste pytest e deve ser executado com o comando:
            task test

    Note:
        - Teste marcado como skip por ser sensível (@pytest.mark.skip)
        - Requer conexão ativa com banco de dados
        - Assume a existência da tabela 'medicines' e da classe MedicinesRepository
        - Realiza limpeza dos dados inseridos após execução
    """
    mocked_medicine = {
        "medicine_id": 1111111111112,
        "product": "product1",
        "substance": "substance1;substance2;substance3",
        "presentation": "presentation1",
        "product_type": "product_type1",
        "ean": 1111111111112,
        "cnpj": 11111111111112,
        "laboratory": "laboratory1",
    }

    sql = f"""
        INSERT INTO medicines (medicine_id, product, substance, presentation, product_type, ean, cnpj, laboratory)
        VALUES (
            {mocked_medicine["medicine_id"]},
            '{mocked_medicine["product"]}',
            '{mocked_medicine["substance"]}',
            '{mocked_medicine["presentation"]}',
            '{mocked_medicine["product_type"]}',
            {mocked_medicine["ean"]},{mocked_medicine["cnpj"]},
            '{mocked_medicine["laboratory"]}')
    """

    connection.execute(text(sql))
    connection.commit()

    medicines_repository = MedicinesRepository()
    response = medicines_repository.select_medicine(mocked_medicine["medicine_id"])

    assert response.medicine_id == mocked_medicine["medicine_id"]
    assert response.product == mocked_medicine["product"]
    assert response.cnpj == mocked_medicine["cnpj"]

    connection.execute(
        text(
            f"""
        DELETE FROM medicines WHERE medicine_id = {response.medicine_id}
    """
        )
    )
    connection.commit()
