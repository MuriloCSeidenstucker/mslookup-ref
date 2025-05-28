from cerberus import Validator

from mslookup_ref.errors.types import HttpUnprocessableEntityError


def laboratory_register_validator(request: any) -> bool:

    body_validator = Validator(
        {
            "full_name": {"type": "string", "required": True, "empty": False},
            "cnpj": {
                "type": "string",
                "required": True,
                "empty": False,
                "regex": r"^\d{14}$",
            },
            "alt_names": {
                "type": "list",
                "required": True,
                "empty": False,
                "schema": { "type": "string", "empty": False, "minlength": 2 },
            },
            "linked": {
                "type": "list",
                "required": False,
                "schema": { "type": "string", "empty": False, "minlength": 2 }},
        }
    )

    response = body_validator.validate(request.json)

    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)

    return response
