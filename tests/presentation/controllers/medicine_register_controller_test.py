# pylint: disable=R0903:too-few-public-methods

from src.presentation.controllers.medicine_register_controller import (
    MedicineRegisterController,
)
from src.presentation.http_types.http_response import HttpResponse
from tests.data.use_cases.medicine_register import MedicineRegisterSpy


class HttpRequestMock:
    """Classe auxiliar para simular uma requisição HTTP nos testes.

    Attributes:
        body (dict): Dicionário contendo parâmetros de consulta simulados.
    """

    def __init__(self) -> None:
        self.body = {
            "medicine_id": 111111111111,
            "product": "product1",
            "substance": "substance1;substance2;substance3",
            "presentation": "presentation1",
            "product_type": "product_type1",
            "ean": 1111111111111,
            "cnpj": 11111111111111,
            "laboratory": "laboratory1",
        }


def test_handle():
    """Testa o método handle do MedicineRegisterController.

    Verifica se o controlador processa corretamente uma requisição HTTP simulada,
    utilizando uma classe espiã (MedicineRegisterSpy) para simular o caso de uso de
    registro de medicamentos. O teste valida que a resposta é uma instância de
    HttpResponse, possui o código de status 200 e contém dados no corpo da resposta.

    Raises:
        AssertionError: Se a resposta não for uma instância de HttpResponse, o código
            de status não for 200, ou o campo 'data' no corpo da resposta for None.
    """

    http_request_mock = HttpRequestMock()
    use_case = MedicineRegisterSpy()
    medicine_register_controller = MedicineRegisterController(use_case)

    response = medicine_register_controller.handle(http_request_mock)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 200
    assert response.body["data"] is not None
