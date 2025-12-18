from cerberus import Validator

from src.errors.types import HttpUnprocessableEntityError


def medicine_register_validator(request: any) -> bool:
    """Valida o corpo de uma requisição para registro de medicamentos.

    Esta função utiliza a biblioteca Cerberus para validar o corpo JSON de uma requisição,
    garantindo que todos os campos obrigatórios para registro de um medicamento estejam
    presentes, com tipos corretos e não vazios. Os campos validados incluem 'medicine_id',
    'product', 'substance', 'presentation', 'product_type', 'ean', 'cnpj' e 'laboratory'.
    Se a validação falhar, lança uma exceção com os detalhes dos erros encontrados.

    Args:
        request (any): Objeto de requisição (ex.: Flask Request) contendo o corpo JSON
            (request.json) com os dados do medicamento.

    Returns:
        bool: True se a validação for bem-sucedida.

    Raises:
        HttpUnprocessableEntityError: Se a validação falhar, contendo os erros de validação
            retornados pelo Cerberus.

    Example:
        - Requisição válida:
            request.json = {
                "medicine_id": "1234567890123",
                "product": "product1",
                "substance": "substance1;substance2;substance3",
                "presentation": "presentation1",
                "product_type": "product_type1",
                "ean": "1111111111111",
                "cnpj": "11111111111111",
                "laboratory": "laboratory1"
            }
            Retorno: True
        - Requisição inválida:
            request.json = {"medicine_id": "abcdef"}
            Levanta: HttpUnprocessableEntityError({
                "medicine_id": ["field cannot be coerced", "must be of integer type"],
                "product": ["required field"],
                ...
            })
    """

    body_validator = Validator(
        {
            "medicine_id": {
                "type": "integer",
                "coerce": int,
                "required": True,
                "empty": False,
            },
            "product": {"type": "string", "required": True, "empty": False},
            "substance": {"type": "string", "required": True, "empty": False},
            "presentation": {"type": "string", "required": True, "empty": False},
            "product_type": {"type": "string", "required": True, "empty": False},
            "ean": {"type": "integer", "coerce": int, "required": True, "empty": False},
            "cnpj": {
                "type": "integer",
                "coerce": int,
                "required": True,
                "empty": False,
            },
            "laboratory": {"type": "string", "required": True, "empty": False},
        }
    )

    response = body_validator.validate(request.json)

    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)

    return response
