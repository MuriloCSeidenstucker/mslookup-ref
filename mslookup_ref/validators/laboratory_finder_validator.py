from cerberus import Validator

from mslookup_ref.errors.types import HttpUnprocessableEntityError


def laboratory_finder_validator(request: any) -> bool:
    query_validator = Validator(
        {
            "cnpj": {
                "type": "string",
                "required": True,
                "empty": False,
                "regex": r"^\d{14}$",
            }
        }
    )

    response = query_validator.validate(dict(request.args))

    if response is False:
        raise HttpUnprocessableEntityError(query_validator.errors)

    return response
