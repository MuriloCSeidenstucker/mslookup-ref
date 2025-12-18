# pylint: disable=C0301:line-too-long, R0903:too-few-public-methods

import pytest

from src.errors.types.http_unprocessable_entity import (
    HttpUnprocessableEntityError,
)
from src.validators.medicine_register_validator import (
    medicine_register_validator,
)


class MockRequest:
    """Classe auxiliar para simular uma requisição nos testes.

    Attributes:
        json (dict): Dicionário simulando o corpo JSON da requisição.
    """

    def __init__(self) -> None:
        self.json = None


def test_medicine_register_validator():
    """Testa a validação bem-sucedida do corpo da requisição para registro de medicamentos.

    Verifica se a função medicine_register_validator valida corretamente uma requisição
    com um corpo JSON contendo todos os campos obrigatórios, incluindo 'medicine_id' como
    inteiro e outros atributos válidos, retornando True.
    """

    request = MockRequest()
    request.json = {
        "medicine_id": "1234567890123",
        "product": "product1",
        "substance": "substance1;substance2;substance3",
        "presentation": "presentation1",
        "product_type": "product_type1",
        "ean": "1111111111111",
        "cnpj": "11111111111111",
        "laboratory": "laboratory1",
    }

    assert medicine_register_validator(request)


def test_medicine_register_validator_not_integer_error():
    """Testa a validação de um 'medicine_id' não inteiro no corpo da requisição.

    Verifica se a função medicine_register_validator lança uma HttpUnprocessableEntityError
    com os erros esperados quando o 'medicine_id' no corpo JSON não é um número inteiro.

    Raises:
        AssertionError: Se a exceção não for lançada ou a mensagem de erro não corresponder
            ao esperado.
    """

    request = MockRequest()
    request.json = {
        "medicine_id": "abcdef",
        "product": "product1",
        "substance": "substance1;substance2;substance3",
        "presentation": "presentation1",
        "product_type": "product_type1",
        "ean": "1111111111111",
        "cnpj": "11111111111111",
        "laboratory": "laboratory1",
    }

    expected_error = {
        "medicine_id": [
            "field 'medicine_id' cannot be coerced: invalid literal for int() with base 10: 'abcdef'",
            "must be of integer type",
        ]
    }

    with pytest.raises(HttpUnprocessableEntityError) as exc_info:
        medicine_register_validator(request)

    assert exc_info.value.message == expected_error


def test_medicine_register_validator_unknown_key_error():
    """Testa a validação de uma chave desconhecida ou ausente no corpo da requisição.

    Verifica se a função medicine_register_validator lança uma HttpUnprocessableEntityError
    com os erros esperados quando o corpo JSON contém uma chave desconhecida ('id') e falta
    a chave obrigatória 'medicine_id'.

    Raises:
        AssertionError: Se a exceção não for lançada ou a mensagem de erro não corresponder
            ao esperado.
    """

    request = MockRequest()
    request.json = {
        "id": "1234567890123",
        "product": "product1",
        "substance": "substance1;substance2;substance3",
        "presentation": "presentation1",
        "product_type": "product_type1",
        "ean": "1111111111111",
        "cnpj": "11111111111111",
        "laboratory": "laboratory1",
    }

    expected_error = {"id": ["unknown field"], "medicine_id": ["required field"]}

    with pytest.raises(HttpUnprocessableEntityError) as exc_info:
        medicine_register_validator(request)

    assert exc_info.value.message == expected_error
