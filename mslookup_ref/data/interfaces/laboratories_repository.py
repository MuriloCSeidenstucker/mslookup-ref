# pylint: disable=C0301:line-too-long

from abc import ABC, abstractmethod

from mslookup_ref.domain.models.laboratories import Laboratories


class LaboratoriesRepositoryInterface(ABC):
    """Define a interface para repositórios de laboratórios.

    Esta classe abstrata estabelece o contrato para implementações de repositórios
    responsáveis por operações de persistência e recuperação de dados de laboratórios.
    As implementações concretas devem fornecer os métodos para inserir e selecionar
    laboratórios.
    """

    @abstractmethod
    def insert_laboratory(self, laboratory: Laboratories) -> int:
        """Insere um laboratório no repositório.

        Args:
            laboratory (Laboratories): Instância do modelo Laboratories contendo os dados do laboratório.

        Raises:
            NotImplementedError: Se o método não for implementado pelas classes derivadas.
        """

    @abstractmethod
    def select_laboratory(self, cnpj: str) -> Laboratories:
        """Seleciona um laboratório pelo seu cnpj.

        Args:
            cnpj (str): cnpj do laboratório a ser recuperado.

        Returns:
            Laboratories: Instância do modelo Laboratories com os dados do laboratório encontrado.

        Raises:
            NotImplementedError: Se o método não for implementado pelas classes derivadas.
        """
