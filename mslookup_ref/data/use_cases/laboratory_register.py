# pylint: disable=R0903:too-few-public-methods, W0511:fixme, C0301:line-too-long

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

    Esta classe é responsável por registrar laboratórios no sistema, utilizando um
    repositório para persistência dos dados. Segue o contrato definido pela interface
    LaboratoryRegisterInterface.

    Args:
        laboratory_repository (LaboratoriesRepositoryInterface): Repositório responsável
            por realizar operações de persistência de laboratórios.

    Attributes:
        __laboratory_repository (LaboratoriesRepositoryInterface): Repositório utilizado
            para operações de persistência de laboratórios.
    """

    def __init__(self, laboratory_repository: LaboratoriesRepositoryInterface) -> None:
        self.__laboratory_repository = laboratory_repository

    def register(self, laboratory: Laboratories) -> Dict:
        """Registra um laboratório no sistema.

        Valida o ID do laboratório, persiste os dados no repositório e retorna uma
        resposta formatada com os dados do laboratório.

        Args:
            laboratory (Laboratories): Instância do modelo Laboratories contendo os dados do laboratório.

        Returns:
            Dict: Dicionário contendo os dados do laboratório registrado.
        """
        self.__validate_laboratory_cnpj(laboratory.cnpj)
        self.__register_laboratory(laboratory)
        response = self.__format_response(laboratory)
        return response

    @classmethod
    def __validate_laboratory_cnpj(cls, cnpj: str) -> None:
        if not cnpj.isdigit():
            raise HttpBadRequestError(
                "O CNPJ do laboratório deve conter apenas números inteiros."
            )

        if len(cnpj) != 14:
            raise HttpBadRequestError("O CNPJ deve conter 14 dígitos.")

    def __register_laboratory(self, laboratory: Laboratories) -> None:
        """Persiste um laboratório no repositório.

        Utiliza o repositório injetado para inserir os dados do laboratório.

        Args:
            laboratory (Laboratories): Instância do modelo Laboratories a ser persistida.
        """
        self.__laboratory_repository.insert_laboratory(laboratory)

    @classmethod
    def __format_response(cls, laboratory: Laboratories) -> Dict:
        """Formata a resposta do registro em um dicionário.

        Cria um dicionário com a estrutura {"type": "Laboratories", "attributes": dict[str, Any]},
        contendo os dados do laboratório registrado.

        Args:
            laboratory (Laboratories): Instância do modelo Laboratories a ser formatada.

        Returns:
            Dict: Dicionário com os dados formatados do laboratório.
        """

        attributes = {
            "full_name": laboratory.full_name,
            "cnpj": laboratory.cnpj,
            "alt_names": laboratory.alt_names,
            "linked": laboratory.linked,
        }
        response = {"type": "Laboratories", "attributes": attributes}
        return response
