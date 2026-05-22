from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.errors.error_handler import handle_errors
from src.errors.types import (
    HttpBadRequestError,
    HttpNotFoundError,
    HttpUnprocessableEntityError,
)
from src.main.routes.routes import router

app = FastAPI(
    title="mslookup",
    description="API para consulta de registros de medicamentos da ANVISA a partir de dados públicos.",
    version="1.0.0",
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
)


@app.exception_handler(HttpBadRequestError)
@app.exception_handler(HttpNotFoundError)
@app.exception_handler(HttpUnprocessableEntityError)
@app.exception_handler(Exception)
async def custom_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    http_response = handle_errors(exc)
    return JSONResponse(
        status_code=http_response.status_code,
        content=http_response.body,
    )


app.include_router(router)
