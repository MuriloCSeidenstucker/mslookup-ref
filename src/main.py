from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.drug_routes import router
from src.core.errors.error_handler import handle_errors
from src.core.errors.types import HttpBadRequestError, HttpNotFoundError
from src.utils.logging import setup_logging

setup_logging()

app = FastAPI(
    title="mslookup",
    description="API para consulta de registros de medicamentos da ANVISA a partir de dados públicos.",
    version="1.0.0",
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
)


@app.exception_handler(HttpBadRequestError)
@app.exception_handler(HttpNotFoundError)
@app.exception_handler(Exception)
async def custom_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    return handle_errors(exc)


app.include_router(router)
