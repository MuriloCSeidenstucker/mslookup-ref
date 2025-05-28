# pylint: disable=R0903:too-few-public-methods, C0115:missing-class-docstring, C0116:missing-function-docstring

from mslookup_ref.presentation.controllers.laboratory_register_controller import (
    LaboratoryRegisterController,
)
from mslookup_ref.presentation.http_types.http_response import HttpResponse
from tests.data.use_cases.laboratory_register import LaboratoryRegisterSpy


class HttpRequestMock:

    def __init__(self) -> None:
        self.body = {
            "full_name": "laboratory_1",
            "cnpj": "12.345.678/9012-34",
            "alt_names": ["lab_1", "laborat_1"],
            "linked": ["laboratory_linked_1"],
        }

def test_handle():

    http_request_mock = HttpRequestMock()
    use_case = LaboratoryRegisterSpy()
    medicine_register_controller = LaboratoryRegisterController(use_case)

    response = medicine_register_controller.handle(http_request_mock)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 200
    assert response.body["data"] is not None
