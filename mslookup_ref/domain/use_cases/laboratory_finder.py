# pylint: disable=R0903:too-few-public-methods

from abc import ABC, abstractmethod
from typing import Dict


class LaboratoryFinder(ABC):
    """Define a interface para casos de uso de busca de laboratórios.

    Esta classe abstrata estabelece o contrato para implementações que buscam
    informações de laboratórios com base no cnpj. É usada como base para
    casos de uso que recuperam dados de laboratórios em formato de dicionário.
    """

    @abstractmethod
    def find(self, cnpj: str) -> Dict:
        """Busca um laboratório pelo seu cnpj.

        Args:
            cnpj (str): cnpj do laboratório a ser buscado.

        Returns:
            Dict: Dicionário contendo os dados do laboratório encontrado.

        Raises:
            NotImplementedError: Se o método não for implementado pelas classes derivadas.
        """
