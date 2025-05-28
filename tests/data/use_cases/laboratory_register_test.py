# pylint: disable=C0116:missing-function-docstring

from mslookup_ref.data.use_cases.laboratory_register import LaboratoryRegister
from mslookup_ref.domain.models.laboratories import Laboratories
from mslookup_ref.errors.types import HttpBadRequestError
from tests.infra.db.repositories.laboratories_repository import LaboratoriesRepositorySpy


def test_register():
    mocked_laboratory = Laboratories(
        full_name = "laboratory_1",
        cnpj = "12345678901234",
        alt_names = ["lab_1", "laborat_1"],
        linked = ["laboratory_linked_1"],
    )

    repo = LaboratoriesRepositorySpy()
    laboratory_register = LaboratoryRegister(repo)

    response = laboratory_register.register(mocked_laboratory)

    assert (
        repo.insert_laboratory_attributes["laboratory"].cnpj
        == mocked_laboratory.cnpj
    )
    assert response["type"] == "Laboratories"
    assert response["attributes"]["full_name"] == mocked_laboratory.full_name


def test_register_validation_error_not_digit():
    mocked_laboratory = Laboratories(
        full_name = "laboratory_1",
        cnpj = "12.345.678/9012-34",
        alt_names = ["lab_1", "laborat_1"],
        linked = ["laboratory_linked_1"],
    )

    repo = LaboratoriesRepositorySpy()
    laboratory_register = LaboratoryRegister(repo)

    try:
        laboratory_register.register(mocked_laboratory)
        assert False, "Expected HttpBadRequestError not raised"
    except HttpBadRequestError as e:
        assert str(e) == "O CNPJ do laboratório deve conter apenas números inteiros."


def test_register_validation_error_not_14_digits():
    mocked_laboratory = Laboratories(
        full_name = "laboratory_1",
        cnpj = "123456789012345",
        alt_names = ["lab_1", "laborat_1"],
        linked = ["laboratory_linked_1"],
    )

    repo = LaboratoriesRepositorySpy()
    laboratory_register = LaboratoryRegister(repo)

    try:
        laboratory_register.register(mocked_laboratory)
        assert False, "Expected HttpBadRequestError not raised"
    except HttpBadRequestError as e:
        assert str(e) == "O CNPJ deve conter 14 dígitos."
