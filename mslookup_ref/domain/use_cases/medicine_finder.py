# pylint: disable=R0903:too-few-public-methods

from abc import ABC, abstractmethod
from typing import Dict


class MedicineFinder(ABC):
    """Define a interface para casos de uso de busca de medicamentos.

    Esta classe abstrata estabelece o contrato para implementações que buscam
    informações de medicamentos com base em um identificador único. É usada como
    base para casos de uso que recuperam dados de medicamentos em formato de dicionário.

    """

    @abstractmethod
    def find(self, medicine_id: int) -> Dict:
        """Busca um medicamento pelo seu identificador único.

        Args:
            medicine_id (int): Identificador único do medicamento a ser buscado.

        Returns:
            Dict: Dicionário contendo os dados do medicamento encontrado.

        Raises:
            NotImplementedError: Se o método não for implementado pelas classes derivadas.
        """
