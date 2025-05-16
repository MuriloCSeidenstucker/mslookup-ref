# pylint: disable=R0903:too-few-public-methods

from sqlalchemy import JSON, BigInteger, Column, String
from sqlalchemy.orm import relationship
from mslookup_ref.infra.db.settings.base import Base


class LaboratoriesEntity(Base):
    """Representa um laboratório no banco de dados.

    Esta classe mapeia os dados dos laboratórios e oferece uma representação
    para consulta e manipulação no banco de dados.
    """

    __tablename__ = "laboratories"

    laboratory_id = Column(BigInteger, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    cnpj = Column(String(14), nullable=False, unique=True)
    alt_names = Column(JSON, nullable=False)
    linked = Column(JSON, nullable=True)

    medicines = relationship(
        "MedicinesEntity",
        back_populates="laboratory",
        order_by="MedicinesEntity.medicine_id"
    )

    def __repr__(self):
        return f"Laboratories [cnpj={self.cnpj}, full_name={self.full_name}]"
