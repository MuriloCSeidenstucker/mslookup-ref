# pylint: disable=R0903:too-few-public-methods, C0301:line-too-long

from src.data.interfaces.medicines_repository import MedicinesRepositoryInterface
from src.domain.models.drugs import Drug
from src.infra.db.entities.drug_entity import DrugEntity
from src.infra.db.settings import DBConnectionHandler


class MedicinesRepository(MedicinesRepositoryInterface):
    """Repositório para operações no banco de dados relacionadas a medicamentos."""

    def insert_medicine(self, medicine: Drug) -> None:
        """Insere um novo registro de medicamento no banco de dados.

        Args:
            medicine (Drug): Objeto contendo os atributos do medicamento a ser inserido.

        Raises:
            Exception: Qualquer erro ocorrido durante a operação de inserção no banco de dados.
        """
        with DBConnectionHandler() as database:
            try:
                new_registry = DrugEntity(
                    medicine_id=medicine.medicine_id,
                    product=medicine.product,
                    substance=medicine.substance,
                    presentation=medicine.presentation,
                    product_type=medicine.product_type,
                    ean=medicine.ean,
                    cnpj=medicine.cnpj,
                    laboratory=medicine.laboratory,
                )
                database.session.add(new_registry)
                database.session.commit()
            except Exception as ex:
                database.session.rollback()
                raise ex

    def select_medicine(self, medicine_id: int) -> Drug:
        """Consulta medicamentos no banco de dados com base no seu identificador único (registro do produto).

        Args:
            medicine_id (int): Identificador único (registro do produto) a ser consultado.

        Returns:
            Drug: Instância da classe Drug contendo os atributos do medicamento encontrado.

        Raises:
            Exception: Qualquer erro ocorrido durante a operação de consulta no banco de dados.
        """
        with DBConnectionHandler() as database:
            try:
                medicines = (
                    database.session.query(DrugEntity)
                    .filter(DrugEntity.medicine_id == medicine_id)
                    .first()
                )
                return medicines
            except Exception as ex:
                database.session.rollback()
                raise ex
