# pylint: disable=R0903:too-few-public-methods

from abc import ABC, abstractmethod

from mslookup_ref.presentation.http_types.http_request import HttpRequest
from mslookup_ref.presentation.http_types.http_response import HttpResponse


class ControllerInterface(ABC):
    """Define a interface para controladores na camada de apresentação.

    Esta classe abstrata estabelece o contrato para implementações de controladores
    que processam requisições HTTP e retornam respostas HTTP. É utilizada na camada
    de apresentação para garantir que todos os controladores sigam um padrão comum
    de manipulação de requisições.
    """

    @abstractmethod
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """Processa uma requisição HTTP e retorna uma resposta HTTP.

        Args:
            http_request (HttpRequest): Objeto contendo os dados da requisição HTTP,
                como cabeçalhos, corpo, parâmetros e URL.

        Returns:
            HttpResponse: Objeto contendo o código de status e o corpo da resposta HTTP.

        Raises:
            NotImplementedError: Se o método não for implementado pelas classes derivadas.
        """
