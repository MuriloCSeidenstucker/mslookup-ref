from typing import Annotated

from fastapi import APIRouter, Depends, Query

from src.repositories.drugs_repository import DrugsRepository
from src.schemas.drug_schemas import DrugResponseSchema
from src.services.drug_finder_service import DrugFinderService


def get_drug_finder_service():
    repository = DrugsRepository()
    return DrugFinderService(repository)


router = APIRouter(prefix="/drugs", tags=["drugs"])
DrugService = Annotated[DrugFinderService, Depends(get_drug_finder_service)]


@router.get("/", response_model=DrugResponseSchema)
def search_drugs(
    service: DrugService,
    product_name: str = Query(...),
    active_ingredient: str | None = Query(None),
    registration_holder: str | None = Query(None),
    regulatory_category: str | None = Query(None),
):
    return service.find(
        product_name=product_name,
        active_ingredient=active_ingredient,
        registration_holder=registration_holder,
        regulatory_category=regulatory_category,
    )
