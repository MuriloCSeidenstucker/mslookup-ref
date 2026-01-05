# pylint: disable=R0903:too-few-public-methods

from src.data.use_cases.drug_finder import DrugFinder
from src.ingest.normalizer import normalize_text
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interfaces.controller_interface import ControllerInterface


class DrugFinderController(ControllerInterface):

    def __init__(self, use_case: DrugFinder) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        query_params = http_request.query_params or {}

        product_name = query_params.get("product_name")
        active_ingredient = query_params.get("active_ingredient")
        registration_holder = query_params.get("registration_holder")

        product_name_normalized = normalize_text(product_name)
        active_ingredient_normalized = normalize_text(active_ingredient)
        registration_holder_normalized = normalize_text(registration_holder)

        response = self.__use_case.find(
            product_name=product_name_normalized,
            active_ingredient=active_ingredient_normalized,
            registration_holder=registration_holder_normalized,
        )

        return HttpResponse(
            status_code=200,
            body={"data": response},
        )
