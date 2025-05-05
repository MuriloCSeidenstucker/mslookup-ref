from mslookup_ref.data.use_cases.medicine_finder import MedicineFinder
from mslookup_ref.infra.db.repositories.medicines_repository import MedicinesRepository
from mslookup_ref.presentation.controllers.medicine_finder_controller import (
    MedicineFinderController,
)


def medicine_finder_composer():
    repository = MedicinesRepository()
    use_case = MedicineFinder(repository)
    controller = MedicineFinderController(use_case)

    return controller.handle
