from src.data.use_cases.medicine_register import MedicineRegister
from src.domain.models.drugs import Medicines
from src.errors.types import HttpBadRequestError
from tests.infra.db.repositories.medicines_repository import MedicinesRepositorySpy


def test_register():
    """Testa o caso de uso de registro de medicamentos.

    Verifica se a classe MedicineRegister registra corretamente um medicamento
    utilizando um repositório espião (spy). O teste valida que o medicamento é
    inserido no repositório com o ID correto e que a resposta retornada contém
    o tipo e os atributos esperados.

    Raises:
        AssertionError: Se o ID do medicamento inserido no repositório não corresponder
            ao ID do medicamento simulado, ou se a resposta não contiver o tipo ou
            atributos esperados.
    """
    mocked_medicine = Medicines(
        medicine_id=1111111111111,
        product="product1",
        substance="substance1;substance2;substance3",
        presentation="presentation1",
        product_type="product_type1",
        ean=1111111111111,
        cnpj=11111111111111,
        laboratory="laboratory1",
    )

    repo = MedicinesRepositorySpy()
    medicine_register = MedicineRegister(repo)

    response = medicine_register.register(mocked_medicine)

    assert (
        repo.insert_medicine_attributes["medicine"].medicine_id
        == mocked_medicine.medicine_id
    )
    assert response["type"] == "Medicines"
    assert response["attributes"]


def test_register_validation_error_not_integer():
    """Testa a validação de erro quando o ID do medicamento não é um número inteiro.

    Verifica se o método `register` da classe `MedicineRegister`
        levanta uma exceção `HttpBadRequestError` com a mensagem correta
        quando o ID fornecido é um número não inteiro.
    """
    mocked_medicine = Medicines(
        medicine_id=1234567890123.0,
        product="product1",
        substance="substance1;substance2;substance3",
        presentation="presentation1",
        product_type="product_type1",
        ean=1111111111111,
        cnpj=11111111111111,
        laboratory="laboratory1",
    )

    repo = MedicinesRepositorySpy()
    medicine_register = MedicineRegister(repo)

    try:
        medicine_register.register(mocked_medicine)
        assert False, "Expected HttpBadRequestError not raised"
    except HttpBadRequestError as e:
        assert str(e) == "O ID do medicamento deve conter apenas números inteiros."


def test_register_validation_error_not_13_digits():
    """Testa a validação de erro quando o ID do medicamento não contém 13 dígitos.

    Verifica se o método `register` da classe `MedicineRegister`
        levanta uma exceção `HttpBadRequestError` com a mensagem correta
        quando o ID fornecido não possui exatamente 13 dígitos.
    """
    mocked_medicine = Medicines(
        medicine_id=12345678901234,
        product="product1",
        substance="substance1;substance2;substance3",
        presentation="presentation1",
        product_type="product_type1",
        ean=1111111111111,
        cnpj=11111111111111,
        laboratory="laboratory1",
    )

    repo = MedicinesRepositorySpy()
    medicine_register = MedicineRegister(repo)

    try:
        medicine_register.register(mocked_medicine)
        assert False, "Expected HttpBadRequestError not raised"
    except HttpBadRequestError as e:
        assert str(e) == "O ID do medicamento deve conter 13 dígitos."
