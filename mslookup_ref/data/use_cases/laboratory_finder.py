# pylint: disable=R0903:too-few-public-methods, C0301:line-too-long

from typing import Dict

from mslookup_ref.data.interfaces.laboratories_repository import (
    LaboratoriesRepositoryInterface,
)
from mslookup_ref.domain.models.laboratories import Laboratories
from mslookup_ref.domain.use_cases.laboratory_finder import (
    LaboratoryFinder as LaboratoryFinderInterface,
)
from mslookup_ref.errors.types import HttpBadRequestError, HttpNotFoundError


class LaboratoryFinder(LaboratoryFinderInterface):
    """Implementa o caso de uso para busca de laboratórios.

    Esta classe realiza a busca de laboratórios por meio de um repositório, validando o
    CNPJ fornecido e retornando os dados em formato de dicionário. Segue o contrato
    definido pela interface LaboratoryFinderInterface, tratando erros específicos com
    exceções padronizadas.

    Args:
        laboratories_repository (LaboratoriesRepositoryInterface): Repositório responsável
            por acessar os dados de laboratórios.

    Attributes:
        __laboratories_repository (LaboratoriesRepositoryInterface): Repositório utilizado
            para operações de busca de laboratórios.
    """

    def __init__(self, laboratories_repository: LaboratoriesRepositoryInterface) -> None:
        self.__laboratories_repository = laboratories_repository

    def find(self, cnpj: str) -> Dict:
        """Busca um laboratório no repositório pelo seu CNPJ.

        Args:
            cnpj (str): CNPJ do laboratório a ser buscado (14 dígitos, apenas números).

        Returns:
            Dict: Dicionário no formato {"type": "Laboratories", "attributes": <atributos do laboratório>}.

        Raises:
            HttpBadRequestError: Se o CNPJ não for composto apenas por dígitos ou não tiver 14 dígitos.
            HttpNotFoundError: Se o laboratório não for encontrado no repositório.
        """
        self.__validate_laboratory_cnpj(cnpj)
        laboratory = self.__fetch_laboratory(cnpj)
        response = self.__format_response(laboratory)
        return response

    @classmethod
    def __validate_laboratory_cnpj(cls, cnpj: str) -> None:
        """Valida o CNPJ do laboratório quanto ao formato e tamanho.

        Args:
            cnpj (str): CNPJ do laboratório a ser validado.

        Raises:
            HttpBadRequestError: Se o CNPJ não for composto apenas por dígitos ou não tiver 14 dígitos.
        """
        if not cnpj.isdigit():
            raise HttpBadRequestError(
                "O CNPJ do laboratório deve conter apenas números inteiros."
            )

        if len(cnpj) != 14:
            raise HttpBadRequestError("O CNPJ deve conter 14 dígitos.")

    def __fetch_laboratory(self, cnpj: str) -> Laboratories:
        """Consulta o repositório para obter os dados de um laboratório.

        Args:
            cnpj (str): CNPJ do laboratório a ser consultado.

        Returns:
            Laboratories: Instância da classe Laboratories contendo os dados do laboratório.

        Raises:
            HttpNotFoundError: Se o laboratório não for encontrado no repositório.
        """
        laboratory = self.__laboratories_repository.select_laboratory(cnpj)
        if not laboratory:
            raise HttpNotFoundError("Laboratório não encontrado.")
        return laboratory

    @classmethod
    def __format_response(cls, laboratory: Laboratories) -> Dict:
        """Formata os dados do laboratório em um dicionário de resposta.

        Args:
            laboratory (Laboratories): Instância da classe Laboratories com os dados do laboratório.

        Returns:
            Dict: Dicionário no formato {"type": "Laboratories", "attributes": <dicionário de atributos>}.
        """
        attributes = {
            "full_name": laboratory.full_name,
            "cnpj": laboratory.cnpj,
            "alt_names": laboratory.alt_names,
            "linked": laboratory.linked,
        }

        response = {"type": "Laboratories", "attributes": attributes}
        return response
