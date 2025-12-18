# pylint: disable=R0903:too-few-public-methods, W0511:fixme, C0301:line-too-long

from typing import Dict

from src.data.interfaces.medicines_repository import MedicinesRepositoryInterface
from src.domain.models.medicines import Medicines
from src.domain.use_cases.medicine_register import (
    MedicineRegister as MedicineRegisterInterface,
)
from src.errors.types import HttpBadRequestError


class MedicineRegister(MedicineRegisterInterface):
    """Implementa o caso de uso para registro de medicamentos.

    Esta classe é responsável por registrar medicamentos no sistema, utilizando um
    repositório para persistência dos dados. Segue o contrato definido pela interface
    MedicineRegisterInterface.

    Args:
        medicines_repository (MedicinesRepositoryInterface): Repositório responsável
            por realizar operações de persistência de medicamentos.

    Attributes:
        __medicines_repository (MedicinesRepositoryInterface): Repositório utilizado
            para operações de persistência de medicamentos.

    Note:
        Validações adicionais para o registro de medicamentos estão pendentes e devem
        ser implementadas conforme necessário.
    """

    def __init__(self, medicines_repository: MedicinesRepositoryInterface) -> None:
        self.__medicines_repository = medicines_repository

    # TODO: Estudar e adicionar todas as validações necessárias para o registro de medicamentos.
    def register(self, medicine: Medicines) -> Dict:
        """Registra um medicamento no sistema.

        Valida o ID do medicamento, persiste os dados no repositório e retorna uma
        resposta formatada com os dados do medicamento.

        Args:
            medicine (Medicines): Instância do modelo Medicines contendo os dados do medicamento.

        Returns:
            Dict: Dicionário contendo os dados do medicamento registrado, com a estrutura
                {"type": "Medicines", "attributes": <objeto Medicines>}.

        Raises:
            HttpBadRequestError: Se o ID do medicamento não for um número inteiro ou não tiver 13 dígitos.
        """
        self.__validate_medicine_id(medicine.medicine_id)
        self.__register_medicine(medicine)
        response = self.__format_response(medicine)
        return response

    @classmethod
    def __validate_medicine_id(cls, medicine_id: int) -> None:
        """Valida o ID do medicamento quanto ao tipo e tamanho.

        Verifica se o ID é um número inteiro e possui exatamente 13 dígitos. Levanta uma
        exceção se alguma dessas condições não for atendida.

        Args:
            medicine_id (int): Identificador do medicamento a ser validado.

        Raises:
            HttpBadRequestError: Se o ID não for um número inteiro ou não tiver 13 dígitos.
        """
        if not isinstance(medicine_id, int):
            raise HttpBadRequestError(
                "O ID do medicamento deve conter apenas números inteiros."
            )

        if len(str(medicine_id)) != 13:
            raise HttpBadRequestError("O ID do medicamento deve conter 13 dígitos.")

    def __register_medicine(self, medicine: Medicines) -> None:
        """Persiste um medicamento no repositório.

        Utiliza o repositório injetado para inserir os dados do medicamento.

        Args:
            medicine (Medicines): Instância do modelo Medicines a ser persistida.
        """
        self.__medicines_repository.insert_medicine(medicine)

    @classmethod
    def __format_response(cls, medicine: Medicines) -> Dict:
        """Formata a resposta do registro em um dicionário.

        Cria um dicionário com a estrutura {"type": "Medicines", "attributes": <objeto Medicines>},
        contendo os dados do medicamento registrado.

        Args:
            medicine (Medicines): Instância do modelo Medicines a ser formatada.

        Returns:
            Dict: Dicionário com os dados formatados do medicamento.
        """
        response = {"type": "Medicines", "attributes": medicine}
        return response
