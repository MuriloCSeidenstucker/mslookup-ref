# pylint: disable=C0115:missing-class-docstring, R0903:too-few-public-methods, C0116:missing-function-docstring

import pytest

from mslookup_ref.errors.types.http_unprocessable_entity import (
    HttpUnprocessableEntityError,
)
from mslookup_ref.validators.laboratory_register_validator import (
    laboratory_register_validator,
)


class MockRequest:

    def __init__(self) -> None:
        self.json = None


def test_laboratory_register_validator():

    request = MockRequest()
    request.json = {
        "full_name": "laboratory_1",
        "cnpj": "12345678901234",
        "alt_names": ["lab_1", "laborat_1"],
        "linked": ["laboratory_linked_1"],
    }

    assert laboratory_register_validator(request)


def test_laboratory_register_validator_not_digit_error():

    request = MockRequest()
    request.json = {
        "full_name": "laboratory_1",
        "cnpj": "12.345.678/9012-34",
        "alt_names": ["lab_1", "laborat_1"],
        "linked": ["laboratory_linked_1"],
    }

    expected_error = {
        "cnpj": [
            "value does not match regex '^\\d{14}$'",
        ]
    }

    with pytest.raises(HttpUnprocessableEntityError) as exc_info:
        laboratory_register_validator(request)

    assert exc_info.value.message == expected_error


def test_laboratory_register_validator_unknown_key_error():

    request = MockRequest()
    request.json = {
        "full_name": "laboratory_1",
        "cnp": "12345678901234",
        "alt_names": ["lab_1", "laborat_1"],
        "linked": ["laboratory_linked_1"],
    }

    expected_error = {"cnp": ["unknown field"], "cnpj": ["required field"]}

    with pytest.raises(HttpUnprocessableEntityError) as exc_info:
        laboratory_register_validator(request)

    assert exc_info.value.message == expected_error
