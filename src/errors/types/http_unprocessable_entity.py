class HttpUnprocessableEntityError(Exception):
    """Exceção para erros de entidade não processável (HTTP 422).

    Esta classe representa erros quando os dados fornecidos em uma requisição são
    sintaticamente corretos, mas semanticamente inválidos, como falhas em validações
    de formato ou regras de negócio. É utilizada para sinalizar que a requisição não
    pode ser processada devido a erros nos dados fornecidos pelo cliente.

    Args:
        message (str): Mensagem descritiva do erro ocorrido, geralmente contendo
            detalhes das falhas de validação.

    Attributes:
        message (str): Mensagem descritiva do erro, incluindo detalhes de validação.
        name (str): Nome do erro, definido como 'UnprocessableEntity'.
        status_code (int): Código de status HTTP associado, definido como 422.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.name = "UnprocessableEntity"
        self.status_code = 422
