# pylint: disable=R0903:too-few-public-methods

from abc import ABC, abstractmethod
from typing import Dict

from mslookup_ref.domain.models.laboratories import Laboratories


class LaboratoryRegister(ABC):
    """Define a interface para casos de uso de registro de laboratórios.

    Esta classe abstrata estabelece o contrato para implementações que realizam
    o registro de laboratórios, recebendo um modelo de laboratório e retornando
    os dados registrados em formato de dicionário.
    """

    @abstractmethod
    def register(self, laboratory: Laboratories) -> Dict:
        """Registra um laboratório no repositório.

        Args:
            laboratory (Laboratories): Instância do modelo Laboratories contendo os dados do laboratório.

        Returns:
            Dict: Dicionário contendo os dados do laboratório registrado.

        Raises:
            NotImplementedError: Se o método não for implementado pelas classes derivadas.
        """
