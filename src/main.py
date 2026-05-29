from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.drug_routes import router
from src.api.errors.error_handler import handle_errors
from src.core.errors.domain_errors import DrugNotFoundError, InvalidFilterError
from src.utils.logging import setup_logging

setup_logging()

app = FastAPI(
    title="mslookup",
    description="API para consulta de registros de medicamentos da ANVISA a partir de dados públicos.",
    version="1.0.0",
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
)


@app.exception_handler(InvalidFilterError)
@app.exception_handler(DrugNotFoundError)
@app.exception_handler(Exception)
async def custom_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    return handle_errors(exc)


app.include_router(router)
