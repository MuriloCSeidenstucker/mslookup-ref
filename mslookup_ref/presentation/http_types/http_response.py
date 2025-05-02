# pylint: disable=C0301:line-too-long, R0903:too-few-public-methods


class HttpResponse:
    """Representa uma resposta HTTP na camada de apresentação.

    Esta classe modela os componentes de uma resposta HTTP, incluindo o código de status
    e o corpo da resposta. É utilizada na camada de apresentação para estruturar os dados
    retornados em respostas a requisições HTTP.

    Args:
        status_code (int): Código de status HTTP da resposta (ex.: 200, 404, 500).
        body (Any): Corpo da resposta, que pode conter dados como dicionários, listas ou outros tipos.

    Attributes:
        status_code (int): Código de status HTTP da resposta.
        body (Any): Corpo da resposta contendo os dados retornados.
    """

    def __init__(self, status_code, body) -> None:
        self.status_code = status_code
        self.body = body
