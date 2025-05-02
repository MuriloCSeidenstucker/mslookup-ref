# pylint: disable=C0301:line-too-long, R0903:too-few-public-methods

from typing import Dict

from mslookup_ref.domain.models.medicines import Medicines


class MedicineFinderSpy:
    """Classe espiã para simular o comportamento do caso de uso MedicineFinder em testes unitários.

    Esta classe atua como um substituto (spy) para o caso de uso MedicineFinder, permitindo
    testar controladores como MedicineFinderController sem dependências externas. Registra
    os parâmetros recebidos no método find e retorna uma resposta simulada com dados de um
    medicamento.

    Attributes:
        find_attributes (dict): Dicionário que armazena os parâmetros passados ao método find,
            permitindo verificar as chamadas realizadas durante os testes.
    """

    def __init__(self) -> None:
        self.find_attributes = {}

    def find(self, medicine_id: int) -> Dict:
        """Simula a busca de um medicamento por ID e registra o parâmetro recebido.

        Armazena o medicine_id no dicionário find_attributes e retorna uma resposta
        simulada contendo um objeto Medicines com dados fixos.

        Args:
            medicine_id (int): Identificador único do medicamento a ser buscado.

        Returns:
            Dict: Dicionário com a estrutura {"type": "Medicines", "attributes": <objeto Medicines>},
                contendo dados simulados de um medicamento.
        """

        self.find_attributes["medicine_id"] = medicine_id

        mocked_medicine = Medicines(
            id=1111111111111,
            product="product1",
            substance="substance1;substance2;substance3",
            presentation="presentation1",
            product_type="product_type1",
            ean=1111111111111,
            cnpj=11111111111111,
            laboratorie="laboratorie1",
        )
        response = {"type": "Medicines", "attributes": mocked_medicine}
        return response
