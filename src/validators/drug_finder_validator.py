from cerberus import Validator

from src.errors.types import HttpUnprocessableEntityError


def drug_finder_validator(request: any) -> bool:

    query_validator = Validator(
        {
            "name": {
                "type": "string",
                "required": True,
                "empty": False,
            },
            "active_ingredient": {
                "type": "string",
                "required": False,
                "empty": False,
            },
            "registration_holder": {
                "type": "string",
                "required": False,
                "empty": False,
            },
        },
        allow_unknown=True,
    )

    query_params = dict(request.query_params)

    is_valid = query_validator.validate(query_params)

    if not is_valid:
        raise HttpUnprocessableEntityError(query_validator.errors)

    return True
