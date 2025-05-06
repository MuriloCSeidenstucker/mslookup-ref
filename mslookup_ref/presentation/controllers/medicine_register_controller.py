# pylint: disable=R0903:too-few-public-methods

from mslookup_ref.domain.models.medicines import Medicines
from mslookup_ref.domain.use_cases.medicine_register import (
    MedicineRegister as MedicineRegisterInterface,
)
from mslookup_ref.presentation.http_types.http_request import HttpRequest
from mslookup_ref.presentation.http_types.http_response import HttpResponse
from mslookup_ref.presentation.interfaces.controller_interface import (
    ControllerInterface,
)


class MedicineRegisterController(ControllerInterface):
    """Controlador para registro de medicamentos na camada de apresentação.

    Esta classe implementa o caso de uso de registro de medicamentos, recebendo uma requisição
    HTTP, extraindo os dados do medicamento do corpo da requisição e retornando uma resposta
    HTTP com os dados registrados. Segue o contrato definido pela interface ControllerInterface.

    Args:
        use_case (MedicineRegisterInterface): Caso de uso responsável por realizar o registro
            de medicamentos.

    Attributes:
        __use_case (MedicineRegisterInterface): Caso de uso injetado para registrar medicamentos.
    """

    def __init__(self, use_case: MedicineRegisterInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """Processa uma requisição HTTP para registrar um medicamento.

        Extrai os dados do medicamento do corpo da requisição, invoca o caso de uso para
        realizar o registro e retorna uma resposta HTTP com os dados registrados.

        Args:
            http_request (HttpRequest): Objeto contendo os dados da requisição HTTP, incluindo
                o corpo com os dados do medicamento no formato {"medicine": <objeto Medicines>}.

        Returns:
            HttpResponse: Resposta HTTP com status 200 e corpo contendo os dados registrados
                no formato {"data": <dicionário do medicamento>}.

        Raises:
            KeyError: Se a chave 'medicine' não estiver presente no corpo da requisição.
        """
        medicine = Medicines(
            medicine_id=http_request.body["medicine_id"],
            product=http_request.body["product"],
            substance=http_request.body["substance"],
            presentation=http_request.body["presentation"],
            product_type=http_request.body["product_type"],
            ean=http_request.body["ean"],
            cnpj=http_request.body["cnpj"],
            laboratory=http_request.body["laboratory"],
        )
        response = self.__use_case.register(medicine)
        return HttpResponse(status_code=200, body={"data": response})
