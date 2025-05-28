# pylint: disable=C0116:missing-function-docstring, C0115:missing-class-docstring

from mslookup_ref.data.use_cases.laboratory_finder import LaboratoryFinder
from mslookup_ref.errors.types import HttpBadRequestError, HttpNotFoundError
from tests.infra.db.repositories.laboratories_repository import LaboratoriesRepositorySpy


def test_find():
    mock_cnpj = "12345678901234"

    repo = LaboratoriesRepositorySpy()
    laboratory_finder = LaboratoryFinder(repo)

    response = laboratory_finder.find(mock_cnpj)

    assert repo.select_laboratory_attributes["cnpj"] == mock_cnpj
    assert response["type"] == "Laboratories"
    assert response["attributes"] is not None


def test_find_validation_error_not_digit():
    mock_cnpj = "12.345.678/9012-34"

    repo = LaboratoriesRepositorySpy()
    laboratory_finder = LaboratoryFinder(repo)

    try:
        laboratory_finder.find(mock_cnpj)
        assert False, "Expected HttpBadRequestError not raised"
    except HttpBadRequestError as e:
        assert str(e) == "O CNPJ do laboratório deve conter apenas números inteiros."


def test_find_validation_error_not_14_digits():
    mock_cnpj = "123456789012345"

    repo = LaboratoriesRepositorySpy()
    laboratory_finder = LaboratoryFinder(repo)

    try:
        laboratory_finder.find(mock_cnpj)
        assert False, "Expected HttpBadRequestError not raised"
    except HttpBadRequestError as e:
        assert str(e) == "O CNPJ deve conter 14 dígitos."


def test_find_validation_error_medicine_not_found():

    class LaboratoriesRepositoryError(LaboratoriesRepositorySpy):
        def select_laboratory(self, cnpj):
            return None

    mock_cnpj = "12345678901234"

    repo = LaboratoriesRepositoryError()
    medicine_finder = LaboratoryFinder(repo)

    try:
        medicine_finder.find(mock_cnpj)
        assert False, "Expected HttpNotFoundError not raised"
    except HttpNotFoundError as e:
        assert str(e) == "Laboratório não encontrado."
