class HttpBadRequestError(Exception):
    """Exceção para erros de requisição inválida (HTTP 400).

    Esta classe representa erros de requisição malformada ou inválida na camada de
    apresentação, como parâmetros ausentes ou dados incorretos. É utilizada para
    sinalizar que a requisição não pode ser processada devido a erros do cliente.

    Args:
        message (str): Mensagem descritiva do erro ocorrido.

    Attributes:
        message (str): Mensagem descritiva do erro.
        name (str): Nome do erro, definido como 'BadRequest'.
        status_code (int): Código de status HTTP associado, definido como 400.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.name = "BadRequest"
        self.status_code = 400
