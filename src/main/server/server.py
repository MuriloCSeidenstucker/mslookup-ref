from fastapi import FastAPI

from src.main.routes.routes import router

app = FastAPI(
    title="mslookup",
    description="API para consulta de registros de medicamentos da ANVISA a partir de dados públicos.",
    version="1.0.0",
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
)

app.include_router(router)
