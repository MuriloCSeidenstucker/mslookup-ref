from src.data.use_cases.medicine_register import MedicineRegister
from src.infra.db.repositories.medicines_repository import MedicinesRepository
from src.presentation.controllers.medicine_register_controller import (
    MedicineRegisterController,
)


def medicine_register_composer():
    """Compõe e retorna o método handle do MedicineRegisterController.

    Esta função atua como uma factory, instanciando e conectando os componentes necessários
    para o caso de uso de registro de medicamentos. Cria um repositório, um caso de uso e um
    controlador, retornando o método handle do controlador pronto para processar requisições
    HTTP.

    Returns:
        Callable: Método handle do MedicineRegisterController, que recebe um HttpRequest e
            retorna um HttpResponse.
    """

    repository = MedicinesRepository()
    use_case = MedicineRegister(repository)
    controller = MedicineRegisterController(use_case)

    return controller.handle
