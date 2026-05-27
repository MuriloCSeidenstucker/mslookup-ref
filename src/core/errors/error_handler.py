from fastapi.responses import JSONResponse

from src.core.errors.types import HttpBadRequestError, HttpNotFoundError


def handle_errors(error: Exception) -> JSONResponse:
    if isinstance(
        error,
        (
            HttpBadRequestError,
            HttpNotFoundError,
        ),
    ):
        return JSONResponse(
            status_code=error.status_code,
            content={"errors": [{"title": error.name, "detail": error.message}]},
        )

    return JSONResponse(
        status_code=500,
        content={
            "errors": [
                {
                    "title": "Internal Server Error",
                    "detail": str(error),
                }
            ]
        },
    )
