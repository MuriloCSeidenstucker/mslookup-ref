# pylint: disable=R0903:too-few-public-methods

from typing import Dict

from mslookup_ref.data.interfaces.medicines_repository import (
    MedicinesRepositoryInterface,
)
from mslookup_ref.domain.models.medicines import Medicines
from mslookup_ref.domain.use_cases.medicine_finder import (
    MedicineFinder as MedicineFinderInterface,
)


class MedicineFinder(MedicineFinderInterface):
    """Implementa o caso de uso para busca de medicamentos.

    Esta classe realiza a busca de medicamentos por meio de um repositório,
    retornando os dados do medicamento em formato de dicionário. Ela segue
    o contrato definido pela interface MedicineFinderInterface.

    Args:
        medicines_repository (MedicinesRepositoryInterface): Repositório responsável
            por acessar os dados de medicamentos.

    Attributes:
        __medicines_repository (MedicinesRepositoryInterface): Repositório utilizado
            para operações de busca de medicamentos.
    """

    def __init__(self, medicines_repository: MedicinesRepositoryInterface) -> None:
        self.__medicines_repository = medicines_repository

    def find(self, medicine_id: int) -> Dict:
        """Busca um medicamento no repositório pelo seu identificador único.

        Valida o ID do medicamento, consulta o repositório para obter os dados do medicamento
        e formata a resposta em um dicionário com tipo e atributos.

        Args:
            medicine_id (int): Identificador único do medicamento a ser buscado.

        Returns:
            Dict: Dicionário contendo o tipo ("Medicines") e os atributos do medicamento.

        Raises:
            ValueError: Se o ID do medicamento for inválido (não inteiro, não possuir 13 dígitos)
                ou se o medicamento não for encontrado no repositório.
        """
        self.__validate_medicine_id(medicine_id)
        medicine = self.__fetch_medicine(medicine_id)
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
            ValueError: Se o ID não for um número inteiro ou não tiver 13 dígitos.
        """
        if not isinstance(medicine_id, int):
            raise ValueError("O ID do medicamento deve conter apenas números inteiros.")

        if len(str(medicine_id)) != 13:
            raise ValueError("O ID do medicamento deve conter 13 dígitos.")

    def __fetch_medicine(self, medicine_id: int) -> Medicines:
        """Consulta o repositório para obter os dados de um medicamento.

        Realiza a busca do medicamento no repositório utilizando o ID fornecido. Levanta
        uma exceção se o medicamento não for encontrado.

        Args:
            medicine_id (int): Identificador único do medicamento a ser consultado.

        Returns:
            Medicines: Instância da classe Medicines contendo os dados do medicamento.

        Raises:
            ValueError: Se o medicamento não for encontrado no repositório.
        """
        medicine = self.__medicines_repository.select_medicine(medicine_id)
        if not medicine:
            raise ValueError("Medicamento não encontrado.")
        return medicine

    @classmethod
    def __format_response(cls, medicine: Medicines) -> Dict:
        """Formata os dados do medicamento em um dicionário de resposta.

        Cria um dicionário com o tipo "Medicines" e os atributos do medicamento fornecido.

        Args:
            medicine (Medicines): Instância da classe Medicines com os dados do medicamento.

        Returns:
            Dict: Dicionário contendo o tipo ("Medicines") e os atributos do medicamento.
        """

        attributes = {
            "medicine_id": medicine.medicine_id,
            "product": medicine.product,
            "substance": medicine.substance,
            "presentation": medicine.presentation,
            "product_type": medicine.product_type,
            "ean": medicine.ean,
            "cnpj": medicine.cnpj,
            "laboratory": medicine.laboratory,
        }

        response = {"type": "Medicines", "attributes": attributes}
        return response
