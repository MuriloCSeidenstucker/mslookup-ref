# pylint: disable=R0903:too-few-public-methods

from src.domain.use_cases.medicine_finder import (
    MedicineFinder as MedicineFinderInterface,
)
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.interfaces.controller_interface import (
    ControllerInterface,
)


class MedicineFinderController(ControllerInterface):
    """Controlador para busca de medicamentos na camada de apresentação.

    Esta classe implementa o caso de uso de busca de medicamentos, recebendo uma requisição
    HTTP, extraindo o ID do medicamento dos parâmetros de consulta e retornando os dados
    do medicamento em uma resposta HTTP. Segue o contrato definido pela interface
    ControllerInterface.

    Args:
        use_case (MedicineFinderInterface): Caso de uso responsável por realizar a busca
            de medicamentos.

    Attributes:
        __use_case (MedicineFinderInterface): Caso de uso injetado para buscar medicamentos.
    """

    def __init__(self, use_case: MedicineFinderInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """Processa uma requisição HTTP para buscar um medicamento.

        Extrai o ID do medicamento dos parâmetros de consulta da requisição, invoca o caso
        de uso para realizar a busca e retorna uma resposta HTTP com os dados encontrados.

        Args:
            http_request (HttpRequest): Objeto contendo os dados da requisição HTTP, incluindo
                os parâmetros de consulta com o ID do medicamento.

        Returns:
            HttpResponse: Resposta HTTP com status 200 e corpo contendo os dados do medicamento
                no formato {"data": <dicionário do medicamento>}.

        Raises:
            KeyError: Se o parâmetro 'medicine_id' não estiver presente nos query_params.
        """

        medicine_id = int(http_request.query_params["medicine_id"])
        response = self.__use_case.find(medicine_id)
        return HttpResponse(status_code=200, body={"data": response})
