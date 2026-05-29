import logging

from fastapi.responses import JSONResponse

from src.core.errors.domain_errors import DrugNotFoundError, InvalidFilterError

logger = logging.getLogger(__name__)


def handle_errors(error: Exception) -> JSONResponse:
    if isinstance(error, DrugNotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "errors": [
                    {
                        "title": "NotFound",
                        "detail": str(error),
                    }
                ]
            },
        )

    if isinstance(error, InvalidFilterError):
        return JSONResponse(
            status_code=400,
            content={
                "errors": [
                    {
                        "title": "BadRequest",
                        "detail": str(error),
                    }
                ]
            },
        )

    logger.error("Internal Server Error: %s", error, exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "errors": [
                {
                    "title": "Internal Server Error",
                    "detail": "Ocorreu um erro interno no servidor. Tente novamente mais tarde.",
                }
            ]
        },
    )
