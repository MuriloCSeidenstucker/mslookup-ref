from src.data.use_cases.drug_finder import DrugFinder
from src.infra.db.repositories.drugs_repository import DrugsRepository
from src.presentation.controllers.drug_finder_controller import DrugFinderController


def drug_finder_composer():

    repository = DrugsRepository()
    use_case = DrugFinder(repository)
    controller = DrugFinderController(use_case)

    return controller.handle
