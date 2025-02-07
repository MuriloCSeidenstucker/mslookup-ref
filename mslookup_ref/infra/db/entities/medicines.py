# pylint: disable=C0301:line-too-long, R0903:too-few-public-methods

from sqlalchemy import Column, Integer, String

from mslookup_ref.infra.db.settings.base import Base


class Medicines(Base):
    """Representa um medicamento no banco de dados.

    Esta classe mapeia os dados dos medicamentos e oferece uma representação
    para consulta e manipulação no banco de dados.
    """

    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, autoincrement=False)
    product = Column(String, nullable=False)
    substance = Column(String, nullable=False)
    presentation = Column(String, nullable=False)
    product_type = Column(String, nullable=False)
    ean = Column(Integer, nullable=False)
    cnpj = Column(Integer, nullable=False)
    laboratorie = Column(String, nullable=False)

    def __repr__(self):
        return f"Medicines [id={self.id}, product={self.product}, laboratorie={self.laboratorie}]"
