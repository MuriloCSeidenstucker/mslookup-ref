# pylint: disable=R0902:too-many-instance-attributes

from dataclasses import dataclass
from typing import Optional

from mslookup_ref.domain.models.laboratories import Laboratories


@dataclass
class Medicines:
    """Representa uma entidade de medicamento com seus atributos principais.

    Esta classe define a estrutura de dados para armazenar informações sobre um medicamento,
    incluindo identificação, detalhes do produto e dados do laboratório associado.

    Attributes:
        medicine_id (int): Identificador único do medicamento.
        product (str): Nome do produto do medicamento.
        substance (str): Substância ativa ou ingrediente principal.
        presentation (str): Forma de apresentação do medicamento.
        product_type (str): Tipo ou categoria do medicamento (genérico, similar, etc).
        ean (int): Código EAN (código de barras).
        laboratory_id (int): Identificador do laboratório associado (chave estrangeira).
        laboratory (Optional[Laboratories]): Objeto representando o laboratório associado (opcional).
    """

    medicine_id: int
    product: str
    substance: str
    presentation: str
    product_type: str
    ean: int
    laboratory_id: int
    laboratory: Optional[Laboratories]
