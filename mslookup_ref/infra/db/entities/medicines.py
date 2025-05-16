# pylint: disable=C0301:line-too-long, R0903:too-few-public-methods

from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from mslookup_ref.infra.db.settings.base import Base


class MedicinesEntity(Base):
    """Representa um medicamento no banco de dados.

    Esta classe mapeia os dados dos medicamentos e oferece uma representação
    para consulta e manipulação no banco de dados.
    """

    __tablename__ = "medicines"

    medicine_id = Column(BigInteger, primary_key=True, autoincrement=False)
    product = Column(String, nullable=False)
    substance = Column(String, nullable=False)
    presentation = Column(String, nullable=False)
    product_type = Column(String, nullable=False)
    ean = Column(BigInteger, nullable=False)
    laboratory_id = Column(BigInteger, ForeignKey("laboratories.laboratory_id"), nullable=False)
    laboratory = relationship("LaboratoriesEntity", back_populates="medicines")

    def __repr__(self):
        return f"Medicines [medicine_id={self.medicine_id}, product={self.product}, laboratory={self.laboratory_id}]"
