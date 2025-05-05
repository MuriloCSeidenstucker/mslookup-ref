from mslookup_ref.data.use_cases.medicine_register import MedicineRegister
from mslookup_ref.infra.db.repositories.medicines_repository import MedicinesRepository
from mslookup_ref.presentation.controllers.medicine_register_controller import (
    MedicineRegisterController,
)


def medicine_register_composer():
    repository = MedicinesRepository()
    use_case = MedicineRegister(repository)
    controller = MedicineRegisterController(use_case)

    return controller.handle
