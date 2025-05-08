from mslookup_ref.presentation.http_types.http_response import HttpResponse

from .types import HttpBadRequestError, HttpNotFoundError, HttpUnprocessableEntityError


def handle_errors(error: Exception) -> HttpResponse:
    """Gerencia erros da aplicação, retornando respostas HTTP padronizadas.

    Esta função processa exceções levantadas durante a execução da aplicação, mapeando-as
    para respostas HTTP com mensagens padronizadas que incluem o tipo e os detalhes do erro.
    Erros rastreados, como HttpBadRequestError e HttpNotFoundError, são mapeados para seus
    respectivos códigos de status (400 e 404). Erros não rastreados são tratados como erros
    internos do servidor, retornando um código de status 500 com a mensagem de erro capturada.

    Args:
        error (Exception): Exceção levantada a ser tratada.

    Returns:
        HttpResponse: Resposta HTTP contendo o código de status e um corpo no formato
            {"errors": [{"title": <nome do erro>, "detail": <mensagem do erro>}]},
            proporcionando rastreabilidade e clareza sobre o erro ocorrido.

    Examples:
        - Para HttpBadRequestError("Parâmetro inválido"):
            HttpResponse(
                status_code=400,
                body={"errors": [{"title": "BadRequest", "detail": "Parâmetro inválido"}]}
            )
        - Para HttpNotFoundError("Medicamento não encontrado"):
            HttpResponse(
                status_code=404,
                body={"errors": [{"title": "NotFound", "detail": "Medicamento não encontrado"}]}
            )
        - Para Exception("Falha inesperada"):
            HttpResponse(
                status_code=500,
                body={"errors": [{"title": "InternalServerError", "detail": "Falha inesperada"}]}
            )
    """

    if isinstance(
        error, (HttpBadRequestError, HttpNotFoundError, HttpUnprocessableEntityError)
    ):
        return HttpResponse(
            status_code=error.status_code,
            body={"errors": [{"title": error.name, "detail": error.message}]},
        )

    return HttpResponse(
        status_code=500,
        body={"errors": [{"title": "Internal Server Error", "detail": str(error)}]},
    )
