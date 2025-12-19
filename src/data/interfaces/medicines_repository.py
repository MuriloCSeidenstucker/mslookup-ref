from abc import ABC, abstractmethod

from src.domain.models.drugs import Drug


class MedicinesRepositoryInterface(ABC):
    """Define a interface para repositórios de medicamentos.

    Esta classe abstrata estabelece o contrato para implementações de repositórios
    responsáveis por operações de persistência e recuperação de dados de medicamentos.
    As implementações concretas devem fornecer os métodos para inserir e selecionar
    medicamentos.

    """

    @abstractmethod
    def insert_medicine(self, medicine: Drug) -> None:
        """Insere um medicamento no repositório.

        Args:
            medicine (Drug): Instância do modelo Drug contendo os dados do medicamento.

        Raises:
            NotImplementedError: Se o método não for implementado pelas classes derivadas.
        """

    @abstractmethod
    def select_medicine(self, medicine_id: int) -> Drug:
        """Seleciona um medicamento pelo seu identificador único.

        Args:
            medicine_id (int): Identificador único do medicamento a ser recuperado.

        Returns:
            Drug: Instância do modelo Drug com os dados do medicamento encontrado.

        Raises:
            NotImplementedError: Se o método não for implementado pelas classes derivadas.
        """
