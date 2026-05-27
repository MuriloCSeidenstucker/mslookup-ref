class HttpNotFoundError(Exception):
    """Exceção para erros de recurso não encontrado (HTTP 404).

    Esta classe representa erros quando um recurso solicitado, como um medicamento,
    não é encontrado no sistema. É utilizada para sinalizar que uma operação não pode
    ser concluída devido à ausência do recurso especificado.

    Args:
        message (str): Mensagem descritiva do erro ocorrido.

    Attributes:
        message (str): Mensagem descritiva do erro.
        name (str): Nome do erro, definido como 'NotFound'.
        status_code (int): Código de status HTTP associado, definido como 404.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.name = "NotFound"
        self.status_code = 404
