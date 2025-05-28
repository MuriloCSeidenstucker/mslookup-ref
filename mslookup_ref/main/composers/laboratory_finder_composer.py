from mslookup_ref.data.use_cases.laboratory_finder import LaboratoryFinder
from mslookup_ref.infra.db.repositories.laboratories_repository import LaboratoriesRepository
from mslookup_ref.presentation.controllers.laboratory_finder_controller import (
    LaboratoryFinderController,
)


def laboratory_finder_composer():

    repository = LaboratoriesRepository()
    use_case = LaboratoryFinder(repository)
    controller = LaboratoryFinderController(use_case)

    return controller.handle
