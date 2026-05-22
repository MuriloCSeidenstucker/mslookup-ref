from src.errors.error_handler import handle_errors
from src.errors.types import (
    HttpBadRequestError,
    HttpNotFoundError,
    HttpUnprocessableEntityError,
)
from src.presentation.http_types.http_response import HttpResponse


def test_handle_errors_http_bad_request():
    error = HttpBadRequestError("Bad Request Message")
    response = handle_errors(error)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 400
    assert response.body == {
        "errors": [
            {
                "title": "BadRequest",
                "detail": "Bad Request Message",
            }
        ]
    }


def test_handle_errors_http_not_found():
    error = HttpNotFoundError("Not Found Message")
    response = handle_errors(error)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 404
    assert response.body == {
        "errors": [
            {
                "title": "NotFound",
                "detail": "Not Found Message",
            }
        ]
    }


def test_handle_errors_http_unprocessable_entity():
    error = HttpUnprocessableEntityError("Unprocessable Entity Message")
    response = handle_errors(error)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 422
    assert response.body == {
        "errors": [
            {
                "title": "UnprocessableEntity",
                "detail": "Unprocessable Entity Message",
            }
        ]
    }


def test_handle_errors_generic_exception():
    error = Exception("Unexpected system failure")
    response = handle_errors(error)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 500
    assert response.body == {
        "errors": [
            {
                "title": "Internal Server Error",
                "detail": "Unexpected system failure",
            }
        ]
    }
