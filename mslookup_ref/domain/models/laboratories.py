# pylint: disable=R0902:too-many-instance-attributes, C0301:line-too-long

from dataclasses import dataclass
from typing import List, Optional

from mslookup_ref.domain.models.medicines import Medicines


@dataclass
class Laboratories:
    """Representa uma entidade de laboratório na camada de domínio.

    Esta classe define a estrutura de dados para armazenar informações sobre um laboratório,
    incluindo identificação, nomes alternativos e laboratórios associados.

    Attributes:
        laboratory_id (int): Identificador único do laboratório.
        full_name (str): Nome completo do laboratório.
        cnpj (str): Número do CNPJ do laboratório (14 dígitos).
        alt_names (List[str]): Lista de nomes alternativos do laboratório.
        linked (Optional[List[int]]): Lista de IDs de laboratórios associados (opcional).
        medicines (Optional[List['Medicines']]): Lista de medicamentos associados ao laboratório (opcional).
    """

    full_name: str
    cnpj: str
    alt_names: List[str]
    linked: Optional[List[int]] = None
    medicines: Optional[List[Medicines]] = None
