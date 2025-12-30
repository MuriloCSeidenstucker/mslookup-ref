from fastapi import FastAPI

from src.main.routes.routes import router as medicine_router

app = FastAPI(title="MS Lookup API")

app.include_router(medicine_router)
