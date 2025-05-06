from typing import Callable

from flask import Request as FlaskRequest

from mslookup_ref.presentation.http_types.http_request import HttpRequest
from mslookup_ref.presentation.http_types.http_response import HttpResponse


def request_adapter(request: FlaskRequest, controller: Callable) -> HttpResponse:
    """Adapta uma requisição Flask para o modelo interno e invoca um controlador.

    Esta função converte uma requisição HTTP recebida pelo Flask (FlaskRequest) em um
    objeto HttpRequest compatível com a arquitetura da aplicação. Em seguida, invoca o
    controlador fornecido, passando o HttpRequest, e retorna a resposta HTTP gerada.

    Args:
        request (FlaskRequest): Objeto da requisição HTTP recebido pelo Flask, contendo
            dados como corpo, cabeçalhos, parâmetros de consulta e URL.
        controller (Callable): Função ou método controlador que processa o HttpRequest e
            retorna um HttpResponse.

    Returns:
        HttpResponse: Resposta HTTP gerada pelo controlador, contendo o código de status
            e o corpo da resposta.

    Note:
        O corpo da requisição é convertido de JSON para um dicionário apenas se request.data
        estiver presente. Caso contrário, o campo body será None.
    """

    body = None
    if request.data:
        body = request.json

    http_request = HttpRequest(
        body=body,
        headers=request.headers,
        query_params=request.args,
        path_params=request.view_args,
        url=request.full_path,
    )

    http_response = controller(http_request)
    return http_response
