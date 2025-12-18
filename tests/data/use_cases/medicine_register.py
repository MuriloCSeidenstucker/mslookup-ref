# pylint: disable=C0301:line-too-long, R0903:too-few-public-methods

from typing import Dict

from src.domain.models.drugs import Medicines


class MedicineRegisterSpy:
    """Classe espiã para simular o comportamento do caso de uso MedicineRegister em testes unitários.

    Esta classe atua como um substituto (spy) para o caso de uso MedicineRegister, permitindo
    testar controladores como MedicineRegisterController sem dependências externas. Registra
    os parâmetros recebidos no método register e retorna uma resposta simulada com dados de um
    medicamento.

    Attributes:
        find_attributes (dict): Dicionário que armazena os parâmetros passados ao método register,
            permitindo verificar as chamadas realizadas durante os testes.
    """

    def __init__(self) -> None:
        self.find_attributes = {}

    def register(self, medicine: Medicines) -> Dict:
        """Simula o registro de um medicamento e registra o parâmetro recebido.

        Armazena o objeto Medicines no dicionário find_attributes e retorna uma resposta
        simulada contendo os dados do medicamento.

        Args:
            medicine (Medicines): Instância do modelo Medicines contendo os dados do medicamento.

        Returns:
            Dict: Dicionário com a estrutura {"type": "Medicines", "attributes": <objeto Medicines>},
                contendo os dados do medicamento recebido.
        """
        self.find_attributes["medicine"] = medicine

        response = {"type": "Medicines", "attributes": medicine}
        return response
