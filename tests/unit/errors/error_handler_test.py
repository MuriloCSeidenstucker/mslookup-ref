import json

from fastapi.responses import JSONResponse

from src.api.errors.error_handler import handle_errors
from src.core.errors.domain_errors import DrugNotFoundError, InvalidFilterError


def test_handle_errors_http_bad_request():
    error = InvalidFilterError("Bad Request Message")
    response = handle_errors(error)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 400
    assert json.loads(response.body) == {
        "errors": [
            {
                "title": "BadRequest",
                "detail": "Bad Request Message",
            }
        ]
    }


def test_handle_errors_http_not_found():
    error = DrugNotFoundError("Not Found Message")
    response = handle_errors(error)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 404
    assert json.loads(response.body) == {
        "errors": [
            {
                "title": "NotFound",
                "detail": "Not Found Message",
            }
        ]
    }


def test_handle_errors_generic_exception():
    error = Exception("Unexpected system failure")
    response = handle_errors(error)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 500
    assert json.loads(response.body) == {
        "errors": [
            {
                "title": "Internal Server Error",
                "detail": "Ocorreu um erro interno no servidor. Tente novamente mais tarde.",
            }
        ]
    }
