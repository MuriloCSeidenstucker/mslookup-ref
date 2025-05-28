# pylint: disable=R0903:too-few-public-methods, C0115:missing-class-docstring, C0116:missing-function-docstring

from mslookup_ref.presentation.controllers.laboratory_finder_controller import (
    LaboratoryFinderController,
)
from mslookup_ref.presentation.http_types.http_response import HttpResponse
from tests.data.use_cases.laboratory_finder import LaboratoryFinderSpy


class HttpRequestMock:

    def __init__(self) -> None:
        self.query_params = {"cnpj": "12345678901234"}


def test_handle():

    http_request_mock = HttpRequestMock()
    use_case = LaboratoryFinderSpy()
    medicine_finder_controller = LaboratoryFinderController(use_case)

    response = medicine_finder_controller.handle(http_request_mock)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 200
    assert response.body["data"] is not None
