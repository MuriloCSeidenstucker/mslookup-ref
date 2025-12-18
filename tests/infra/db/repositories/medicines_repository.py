# pylint: disable=R0903:too-few-public-methods, C0301:line-too-long

from src.domain.models.medicines import Medicines


class MedicinesRepositorySpy:
    """Classe espiã para simular um repositório de medicamentos, usada para fins de teste.

    Esta classe imita o comportamento de um repositório de medicamentos, armazenando atributos para operações de
    inserção e seleção sem interagir com um banco de dados real. Ela é projetada para capturar entradas e retornar
    saídas predefinidas para testes.

    Attributes:
        insert_medicine_attributes (dict): Armazena os atributos passados para o método insert_medicine.
        select_medicine_attributes (dict): Armazena os atributos passados para o método select_medicine.
    """

    def __init__(self) -> None:
        self.insert_medicine_attributes = {}
        self.select_medicine_attributes = {}

    def insert_medicine(self, medicine: Medicines) -> None:
        """Simula a inserção de um medicamento no repositório.

        Args:
            medicine (Medicines): O objeto de medicamento a ser inserido.

        Armazena os atributos do medicamento como um dicionário em insert_medicine_attributes.
        """
        self.insert_medicine_attributes["medicine"] = medicine

    def select_medicine(self, medicine_id: int) -> Medicines:
        """Simula a consulta de medicamentos no banco de dados com base no seu identificador único (registro do produto).

        Args:
            medicine_id (int): Número do identificador único (registro do produto) a ser pesquisado.

        Returns:
            Medicines: Um objeto Medicines com atributos espiões predefinidos.

        Armazena o medicine_id em select_medicine_attributes.
        """
        self.select_medicine_attributes["medicine_id"] = medicine_id
        return Medicines(
            medicine_id=medicine_id,
            product="product_spy_1",
            substance="substance_spy_1",
            presentation="presentation_spy_1",
            product_type="product_type_spy_1",
            ean=1111111111111,
            cnpj=11111111111111,
            laboratory="laboratory_spy_1",
        )
