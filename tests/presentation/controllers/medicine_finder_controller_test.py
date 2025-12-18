# pylint: disable=R0903:too-few-public-methods

from src.presentation.controllers.medicine_finder_controller import (
    MedicineFinderController,
)
from src.presentation.http_types.http_response import HttpResponse
from tests.data.use_cases.medicine_finder import MedicineFinderSpy


class HttpRequestMock:
    """Classe auxiliar para simular uma requisição HTTP nos testes.

    Attributes:
        query_params (dict): Dicionário contendo parâmetros de consulta simulados,
            incluindo o 'medicine_id'.
    """

    def __init__(self) -> None:
        self.query_params = {"medicine_id": 1234567890123}


def test_handle():
    """Testa o método handle do MedicineFinderController.

    Verifica se o controlador processa corretamente uma requisição HTTP simulada,
    utilizando uma classe espiã (MedicineFinderSpy) para simular o caso de uso.
    O teste valida que a resposta é uma instância de HttpResponse, possui o código
    de status 200 e contém dados no corpo da resposta.

    Raises:
        AssertionError: Se a resposta não for uma instância de HttpResponse, o código
            de status não for 200, ou o campo 'data' no corpo da resposta for None.
    """

    http_request_mock = HttpRequestMock()
    use_case = MedicineFinderSpy()
    medicine_finder_controller = MedicineFinderController(use_case)

    response = medicine_finder_controller.handle(http_request_mock)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 200
    assert response.body["data"] is not None
