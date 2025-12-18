from src.data.use_cases.medicine_finder import MedicineFinder
from src.infra.db.repositories.medicines_repository import MedicinesRepository
from src.presentation.controllers.medicine_finder_controller import (
    MedicineFinderController,
)


def medicine_finder_composer():
    """Compõe e retorna o método handle do MedicineFinderController.

    Esta função atua como uma factory, instanciando e conectando os componentes necessários
    para o caso de uso de busca de medicamentos. Cria um repositório, um caso de uso e um
    controlador, retornando o método handle do controlador pronto para processar requisições
    HTTP.

    Returns:
        Callable: Método handle do MedicineFinderController, que recebe um HttpRequest e
            retorna um HttpResponse.
    """

    repository = MedicinesRepository()
    use_case = MedicineFinder(repository)
    controller = MedicineFinderController(use_case)

    return controller.handle
