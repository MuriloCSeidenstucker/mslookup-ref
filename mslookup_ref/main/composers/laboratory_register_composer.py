from mslookup_ref.data.use_cases.laboratory_register import LaboratoryRegister
from mslookup_ref.infra.db.repositories.laboratories_repository import LaboratoriesRepository
from mslookup_ref.presentation.controllers.laboratory_register_controller import (
    LaboratoryRegisterController,
)


def laboratory_register_composer():

    repository = LaboratoriesRepository()
    use_case = LaboratoryRegister(repository)
    controller = LaboratoryRegisterController(use_case)

    return controller.handle
