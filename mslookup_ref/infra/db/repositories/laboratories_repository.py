# pylint: disable=R0903:too-few-public-methods, C0301:line-too-long

from mslookup_ref.domain.models.laboratories import Laboratories
from mslookup_ref.infra.db.entities.laboratories import LaboratoriesEntity
from mslookup_ref.infra.db.settings import DBConnectionHandler


class LaboratoriesRepository():
    """Repositório para operações no banco de dados relacionadas aos laboratórios."""

    def insert_laboratory(self, laboratory: Laboratories) -> int:
        """Insere um novo registro de laboratório no banco de dados.

        Args:
            laboratory Laboratories: Objeto contendo os dados do laboratório a ser inserido.

        Returns:
            int: Identificador único (ID) do laboratório recém-inserido.            

        Raises:
            Exception: Qualquer erro ocorrido durante a operação de inserção no banco de dados.
        """

        with DBConnectionHandler() as database:
            try:
                new_registry = LaboratoriesEntity(
                    full_name=laboratory.full_name,
                    cnpj=laboratory.cnpj,
                    alt_names=laboratory.alt_names,
                    linked=laboratory.linked,
                )
                database.session.add(new_registry)
                database.session.commit()
                return new_registry.laboratory_id
            except Exception as ex:
                database.session.rollback()
                raise ex

    def select_laboratory(self, cnpj: str) -> Laboratories:
        """Consulta laboratórios no banco de dados com base no cnpj.

        Args:
            cnpj (str): cnpj a ser consultado.

        Returns:
            Laboratories: Objeto contendo os dados do laboratório encontrado.

        Raises:
            Exception: Qualquer erro ocorrido durante a operação de consulta no banco de dados.
        """

        with DBConnectionHandler() as database:
            try:
                laboratory = (
                    database.session.query(LaboratoriesEntity)
                    .filter(LaboratoriesEntity.cnpj == cnpj)
                    .first()
                )
                return laboratory
            except Exception as ex:
                database.session.rollback()
                raise ex
