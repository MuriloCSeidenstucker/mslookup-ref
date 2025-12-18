# pylint: disable=C0301:line-too-long, R0903:too-few-public-methods

import pytest

from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError
from src.validators.medicine_finder_validator import medicine_finder_validator


class MockRequest:
    """Classe auxiliar para simular uma requisição nos testes.

    Attributes:
        args (dict): Dicionário simulando os parâmetros de consulta da requisição.
    """

    def __init__(self) -> None:
        self.args = None


def test_medicine_finder_validator():
    """Testa a validação bem-sucedida dos parâmetros de consulta para busca de medicamentos.

    Verifica se a função medicine_finder_validator valida corretamente uma requisição
    com um 'medicine_id' válido (inteiro com 13 dígitos), retornando True.
    """

    request = MockRequest()
    request.args = {"medicine_id": "1234567890123"}

    assert medicine_finder_validator(request)


def test_medicine_finder_validator_not_integer_error():
    """Testa a validação de um 'medicine_id' não inteiro.

    Verifica se a função medicine_finder_validator lança uma HttpUnprocessableEntityError
    com os erros esperados quando o 'medicine_id' não é um número inteiro.

    Raises:
        AssertionError: Se a exceção não for lançada ou a mensagem de erro não corresponder
            ao esperado.
    """

    request = MockRequest()
    request.args = {"medicine_id": "abcdef"}

    expected_error = {
        "medicine_id": [
            "field 'medicine_id' cannot be coerced: invalid literal for int() with base 10: 'abcdef'",
            "must be of integer type",
        ]
    }

    with pytest.raises(HttpUnprocessableEntityError) as exc_info:
        medicine_finder_validator(request)

    assert exc_info.value.message == expected_error


def test_medicine_finder_validator_unknown_key_error():
    """Testa a validação de uma chave desconhecida ou ausente.

    Verifica se a função medicine_finder_validator lança uma HttpUnprocessableEntityError
    com os erros esperados quando a requisição contém uma chave desconhecida ('id') e
    falta a chave obrigatória 'medicine_id'.

    Raises:
        AssertionError: Se a exceção não for lançada ou a mensagem de erro não corresponder
            ao esperado.
    """

    request = MockRequest()
    request.args = {"id": "1234567890123"}

    expected_error = {"id": ["unknown field"], "medicine_id": ["required field"]}

    with pytest.raises(HttpUnprocessableEntityError) as exc_info:
        medicine_finder_validator(request)

    assert exc_info.value.message == expected_error
