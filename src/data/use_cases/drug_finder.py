# pylint: disable=R0903:too-few-public-methods

from typing import Dict, List, Optional

from src.data.interfaces.drugs_repository_interface import DrugsRepositoryInterface
from src.domain.models.drugs import Drug
from src.domain.use_cases.drug_finder_interface import DrugFinderInterface
from src.errors.types import HttpBadRequestError, HttpNotFoundError


class DrugFinder(DrugFinderInterface):

    def __init__(self, drugs_repository: DrugsRepositoryInterface) -> None:
        self.__drugs_repository = drugs_repository

    def find(
        self,
        *,
        name: str,
        active_ingredient: Optional[str] = None,
        registration_holder: Optional[str] = None,
    ) -> Dict:
        self.__validate_input(name)

        drugs = self.__drugs_repository.find_drugs(
            product_name_normalized=name,
            active_ingredient_normalized=active_ingredient,
            registration_holder_normalized=registration_holder,
            only_valid=True,
        )

        if not drugs:
            raise HttpNotFoundError("Nenhum registro ANVISA encontrado.")

        return self.__format_response(drugs)

    @classmethod
    def __validate_input(cls, name: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise HttpBadRequestError(
                "O nome do medicamento é obrigatório para a busca."
            )

    @classmethod
    def __format_response(cls, drugs: List[Drug]) -> Dict:
        return {
            "type": "DrugRegistrations",
            "count": len(drugs),
            "attributes": [
                {
                    "registration_number": drug.registration_number,
                    "product_name": drug.product_name,
                    "active_ingredient": drug.active_ingredient,
                    "registration_holder": drug.registration_holder,
                    "regulatory_category": drug.regulatory_category,
                    "registration_status": drug.registration_status,
                    "expiration_date": (
                        drug.registration_expiration_date.isoformat()
                        if drug.registration_expiration_date
                        else None
                    ),
                }
                for drug in drugs
            ],
        }
