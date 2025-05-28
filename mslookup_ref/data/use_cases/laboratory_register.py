# pylint: disable=R0903:too-few-public-methods, C0301:line-too-long

from typing import Dict

from mslookup_ref.data.interfaces.laboratories_repository import (
    LaboratoriesRepositoryInterface,
)
from mslookup_ref.domain.models.laboratories import Laboratories
from mslookup_ref.domain.use_cases.laboratory_register import (
    LaboratoryRegister as LaboratoryRegisterInterface,
)
from mslookup_ref.errors.types import HttpBadRequestError


class LaboratoryRegister(LaboratoryRegisterInterface):
    """Implementa o caso de uso para registro de laboratórios.

    Esta classe realiza o registro de laboratórios por meio de um repositório, validando
    o CNPJ do laboratório e inserindo os dados no banco de dados. Segue o contrato
    definido pela interface LaboratoryRegisterInterface, tratando erros de validação
    com exceções padronizadas.

    Args:
        laboratory_repository (LaboratoriesRepositoryInterface): Repositório responsável
            por acessar e manipular os dados de laboratórios.

    Attributes:
        __laboratory_repository (LaboratoriesRepositoryInterface): Repositório utilizado
            para operações de registro de laboratórios.
    """

    def __init__(self, laboratory_repository: LaboratoriesRepositoryInterface) -> None:
        self.__laboratory_repository = laboratory_repository

    def register(self, laboratory: Laboratories) -> Dict:
        """Registra um laboratório no repositório.

        Args:
            laboratory (Laboratories): Instância da classe Laboratories contendo os dados
                do laboratório a ser registrado.

        Returns:
            Dict: Dicionário no formato {"type": "Laboratories", "attributes": <atributos do laboratório>}.

        Raises:
            HttpBadRequestError: Se o CNPJ do laboratório não for composto apenas por dígitos
                ou não tiver 14 dígitos.
        """
        self.__validate_laboratory_cnpj(laboratory.cnpj)
        self.__register_laboratory(laboratory)
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

    def __register_laboratory(self, laboratory: Laboratories) -> None:
        """Insere os dados de um laboratório no repositório.

        Args:
            laboratory (Laboratories): Instância da classe Laboratories contendo os dados
                do laboratório a ser inserido.
        """
        self.__laboratory_repository.insert_laboratory(laboratory)

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
