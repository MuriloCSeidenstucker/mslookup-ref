from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.drug_schemas import DrugQuerySchema, DrugResponseSchema
from src.infra.db.settings.connection import get_session
from src.repositories.drugs_repository import DrugsRepository
from src.services.drug_finder_service import DrugFinderService


def get_drug_finder_service(session: Annotated[Session, Depends(get_session)]):
    repository = DrugsRepository(session)
    return DrugFinderService(repository)


router = APIRouter(prefix="/drugs", tags=["drugs"])
DrugService = Annotated[DrugFinderService, Depends(get_drug_finder_service)]


@router.get("/", response_model=DrugResponseSchema)
def search_drugs(
    service: DrugService,
    query: DrugQuerySchema = Depends(),
):
    return service.find(
        product_name=query.product_name,
        active_ingredient=query.active_ingredient,
        registration_holder=query.registration_holder,
        regulatory_category=query.regulatory_category,
    )
