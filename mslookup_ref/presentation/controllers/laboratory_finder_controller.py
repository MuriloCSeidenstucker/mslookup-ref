# pylint: disable=R0903:too-few-public-methods

from mslookup_ref.domain.use_cases.laboratory_finder import (
    LaboratoryFinder as LaboratoryFinderInterface,
)
from mslookup_ref.presentation.http_types.http_request import HttpRequest
from mslookup_ref.presentation.http_types.http_response import HttpResponse
from mslookup_ref.presentation.interfaces.controller_interface import (
    ControllerInterface,
)


class LaboratoryFinderController(ControllerInterface):

    def __init__(self, use_case: LaboratoryFinderInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:

        cnpj = http_request.query_params["cnpj"]
        response = self.__use_case.find(cnpj)
        return HttpResponse(status_code=200, body={"data": response})
