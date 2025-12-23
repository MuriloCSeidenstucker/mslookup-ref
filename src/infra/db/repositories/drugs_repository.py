from typing import Iterable

from src.domain.models.drugs import Drug
from src.infra.db.entities.drug_entity import DrugEntity
from src.infra.db.settings.connection import DBConnectionHandler


class DrugsRepository:

    def insert_drug(self, drugs: Iterable[Drug]) -> None:
        with DBConnectionHandler() as database:
            try:
                entities = [
                    DrugEntity(
                        registration_number=drug.registration_number,
                        product_name=drug.product_name,
                        product_name_normalized=drug.product_name_normalized,
                        active_ingredient=drug.active_ingredient,
                        active_ingredient_normalized=drug.active_ingredient_normalized,
                        regulatory_category=drug.regulatory_category,
                        regulatory_category_normalized=drug.regulatory_category_normalized,
                        registration_holder=drug.registration_holder,
                        registration_holder_normalized=drug.registration_holder_normalized,
                        registration_status=drug.registration_status,
                        registration_expiration_date=drug.registration_expiration_date,
                        is_registration_valid=drug.is_registration_valid,
                    )
                    for drug in drugs
                ]

                database.session.add_all(entities)
                database.session.commit()

            except Exception:
                database.session.rollback()
                raise
