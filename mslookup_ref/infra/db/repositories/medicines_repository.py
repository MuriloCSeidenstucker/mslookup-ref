# pylint: disable=R0903:too-few-public-methods

from mslookup_ref.infra.db.entities.medicines import Medicines
from mslookup_ref.infra.db.settings import DBConnectionHandler


class MedicinesRepository:
    """Repositório para operações no banco de dados relacionadas a medicamentos."""

    @classmethod
    def insert_medicine(cls, **kwargs) -> None:
        """Insere um novo registro de medicamento no banco de dados.

        Args:
            **kwargs: Parâmetros correspondentes aos atributos do modelo Medicines.
        """
        with DBConnectionHandler() as database:
            try:
                new_registry = Medicines(**kwargs)
                database.session.add(new_registry)
                database.session.commit()
            except Exception as ex:
                database.session.rollback()
                raise ex
