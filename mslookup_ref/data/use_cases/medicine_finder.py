# pylint: disable=R0903:too-few-public-methods

from typing import Dict

from mslookup_ref.data.interfaces.medicines_repository import (
    MedicinesRepositoryInterface,
)
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
        pass
