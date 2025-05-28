# pylint: disable=R0903:too-few-public-methods

from mslookup_ref.domain.models.laboratories import Laboratories
from mslookup_ref.domain.use_cases.laboratory_register import (
    LaboratoryRegister as LaboratoryRegisterInterface,
)
from mslookup_ref.presentation.http_types.http_request import HttpRequest
from mslookup_ref.presentation.http_types.http_response import HttpResponse
from mslookup_ref.presentation.interfaces.controller_interface import (
    ControllerInterface,
)


class LaboratoryRegisterController(ControllerInterface):

    def __init__(self, use_case: LaboratoryRegisterInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        laboratory = Laboratories(
            full_name=http_request.body["full_name"],
            cnpj=http_request.body["cnpj"],
            alt_names=http_request.body["alt_names"],
            linked=http_request.body["linked"],
        )
        response = self.__use_case.register(laboratory)
        return HttpResponse(status_code=200, body={"data": response})
