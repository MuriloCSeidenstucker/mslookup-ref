from src.domain.models.drugs import Drug as DrugDomain
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.drug_entity import DrugEntity


class DrugsRepository:
    def insert_drug(self, drug: DrugDomain) -> None:
        with DBConnectionHandler() as database:
            try:
                entity = DrugEntity(
                    registration_number=drug.registration_number,
                    product_name=drug.product_name,
                    active_ingredient=drug.active_ingredient,
                    regulatory_category=drug.regulatory_category,
                    registration_holder=drug.registration_holder,
                    registration_status=drug.registration_status,
                    registration_expiration_date=drug.registration_expiration_date,
                    is_registration_valid=drug.is_registration_valid,
                )

                database.session.add(entity)
                database.session.commit()

            except Exception:
                database.session.rollback()
                raise
