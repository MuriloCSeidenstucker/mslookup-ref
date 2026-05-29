from src.core.errors.domain_errors import DrugNotFoundError
from src.core.models.drugs import Drug
from src.repositories.drugs_repository import DrugsRepository
from src.utils.normalizer import normalize_text


class DrugFinderService:
    def __init__(self, repository: DrugsRepository):
        self.__repository = repository

    def find(
        self,
        product_name: str,
        active_ingredient: str | None = None,
        registration_holder: str | None = None,
        regulatory_category: str | None = None,
    ) -> dict:
        product_name_normalized = normalize_text(product_name)
        active_ingredient_normalized = normalize_text(active_ingredient)
        registration_holder_normalized = normalize_text(registration_holder)
        regulatory_category_normalized = normalize_text(regulatory_category)

        drugs = self.__repository.find_drugs(
            product_name_normalized=product_name_normalized,
            active_ingredient_normalized=active_ingredient_normalized,
            registration_holder_normalized=registration_holder_normalized,
            regulatory_category_normalized=regulatory_category_normalized,
            only_valid=True,
        )

        if not drugs:
            raise DrugNotFoundError("Nenhum registro ANVISA encontrado.")

        return self.__format_response(drugs)

    @classmethod
    def __format_response(cls, drugs: list[Drug]) -> dict:
        return {
            "count": len(drugs),
            "data": [
                {
                    "registration_number": drug.registration_number,
                    "product_name": drug.product_name,
                    "active_ingredient": drug.active_ingredient,
                    "registration_holder": drug.registration_holder,
                    "regulatory_category": drug.regulatory_category,
                    "expiration_date": (
                        drug.registration_expiration_date.isoformat()
                        if drug.registration_expiration_date
                        else None
                    ),
                }
                for drug in drugs
            ],
        }
