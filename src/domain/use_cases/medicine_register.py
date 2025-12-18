# pylint: disable=R0903:too-few-public-methods

from abc import ABC, abstractmethod
from typing import Dict

from src.domain.models.medicines import Medicines


class MedicineRegister(ABC):
    """Define a interface para casos de uso de registro de medicamentos.

    Esta classe abstrata estabelece o contrato para implementações que realizam
    o registro de medicamentos, recebendo um modelo de medicamento e retornando
    os dados registrados em formato de dicionário.

    """

    @abstractmethod
    def register(self, medicine: Medicines) -> Dict:
        """Registra um medicamento no repositório.

        Args:
            medicine (Medicines): Instância do modelo Medicines contendo os dados do medicamento.

        Returns:
            Dict: Dicionário contendo os dados do medicamento registrado.

        Raises:
            NotImplementedError: Se o método não for implementado pelas classes derivadas.
        """
