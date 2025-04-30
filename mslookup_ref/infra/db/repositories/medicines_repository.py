# pylint: disable=R0903:too-few-public-methods, C0301:line-too-long

from mslookup_ref.data.interfaces.medicines_repository import (
    MedicinesRepositoryInterface,
)
from mslookup_ref.domain.models.medicines import Medicines
from mslookup_ref.infra.db.entities.medicines import Medicines as MedicinesEntity
from mslookup_ref.infra.db.settings import DBConnectionHandler


class MedicinesRepository(MedicinesRepositoryInterface):
    """Repositório para operações no banco de dados relacionadas a medicamentos."""

    def insert_medicine(self, medicine: Medicines) -> None:
        """Insere um novo registro de medicamento no banco de dados.

        Args:
            medicine: Parâmetros correspondentes aos atributos do modelo Medicines.
        """
        with DBConnectionHandler() as database:
            try:
                new_registry = MedicinesEntity(
                    id=medicine.id,
                    product=medicine.product,
                    substance=medicine.substance,
                    presentation=medicine.presentation,
                    product_type=medicine.product_type,
                    ean=medicine.ean,
                    cnpj=medicine.cnpj,
                    laboratorie=medicine.laboratorie,
                )
                database.session.add(new_registry)
                database.session.commit()
            except Exception as ex:
                database.session.rollback()
                raise ex

    def select_medicine(self, medicine_id: int) -> Medicines:
        """Consulta medicamentos no banco de dados com base no seu identificador único (registro do produto).

        Args:
            medicine_id (int): Número do identificador único (registro do produto) a ser pesquisado.
        """
        with DBConnectionHandler() as database:
            try:
                medicines = (
                    database.session.query(MedicinesEntity)
                    .filter(MedicinesEntity.id == medicine_id)
                    .all()
                )
                return medicines
            except Exception as ex:
                database.session.rollback()
                raise ex
