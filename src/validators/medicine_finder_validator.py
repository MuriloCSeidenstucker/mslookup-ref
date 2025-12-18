from cerberus import Validator

from src.errors.types import HttpUnprocessableEntityError


def medicine_finder_validator(request: any) -> bool:
    """Valida os parâmetros de consulta de uma requisição para busca de medicamentos.

    Esta função utiliza a biblioteca Cerberus para validar o parâmetro 'medicine_id' em
    uma requisição, garantindo que seja um número inteiro, não vazio e presente nos
    parâmetros de consulta. Se a validação falhar, lança uma exceção com os detalhes dos
    erros encontrados.

    Args:
        request (any): Objeto de requisição (ex.: Flask Request) contendo os parâmetros
            de consulta (request.args).

    Returns:
        bool: True se a validação for bem-sucedida.

    Raises:
        HttpUnprocessableEntityError: Se a validação falhar, contendo os erros de validação
            retornados pelo Cerberus.

    Example:
        - Requisição válida: request.args = {"medicine_id": "1234567890123"}
            Retorno: True
        - Requisição inválida: request.args = {"medicine_id": ""}
            Levanta: HttpUnprocessableEntityError({"medicine_id": ["must not be empty"]})
    """

    query_validator = Validator(
        {
            "medicine_id": {
                "type": "integer",
                "coerce": int,
                "required": True,
                "empty": False,
            }
        }
    )

    response = query_validator.validate(dict(request.args))

    if response is False:
        raise HttpUnprocessableEntityError(query_validator.errors)

    return response
