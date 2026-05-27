from typing import Iterable

from sqlalchemy import select

from src.core.models.drugs import Drug
from src.infra.db.entities.drug_entity import DrugEntity
from src.infra.db.settings.connection import DBConnectionHandler


class DrugsRepository:

    def insert_drugs(self, drugs: Iterable[Drug]) -> None:
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

    def find_drugs(
        self,
        *,
        product_name_normalized: str,
        active_ingredient_normalized: str | None = None,
        registration_holder_normalized: str | None = None,
        regulatory_category_normalized: str | None = None,
        only_valid: bool = True,
        limit: int = 20,
    ) -> list[Drug]:
        with DBConnectionHandler() as database:
            stmt = select(DrugEntity).where(
                DrugEntity.product_name_normalized.like(f"%{product_name_normalized}%")
            )

            if active_ingredient_normalized:
                stmt = stmt.where(
                    DrugEntity.active_ingredient_normalized.like(
                        f"%{active_ingredient_normalized}%"
                    )
                )

            if registration_holder_normalized:
                stmt = stmt.where(
                    DrugEntity.registration_holder_normalized.like(
                        f"%{registration_holder_normalized}%"
                    )
                )

            if regulatory_category_normalized:
                stmt = stmt.where(
                    DrugEntity.regulatory_category_normalized.like(
                        f"%{regulatory_category_normalized}%"
                    )
                )

            if only_valid:
                stmt = stmt.where(DrugEntity.is_registration_valid.is_(True))

            stmt = stmt.limit(limit)

            results = database.session.execute(stmt).scalars().all()

            return [
                Drug(
                    registration_number=entity.registration_number,
                    product_name=entity.product_name,
                    product_name_normalized=entity.product_name_normalized,
                    active_ingredient=entity.active_ingredient,
                    active_ingredient_normalized=entity.active_ingredient_normalized,
                    regulatory_category=entity.regulatory_category,
                    regulatory_category_normalized=entity.regulatory_category_normalized,
                    registration_holder=entity.registration_holder,
                    registration_holder_normalized=entity.registration_holder_normalized,
                    registration_status=entity.registration_status,
                    registration_expiration_date=entity.registration_expiration_date,
                    is_registration_valid=entity.is_registration_valid,
                )
                for entity in results
            ]
