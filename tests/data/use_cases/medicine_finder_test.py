from mslookup_ref.data.use_cases.medicine_finder import MedicineFinder
from tests.infra.db.repositories.medicines_repository import MedicinesRepositorySpy


def test_find():
    """Testa a funcionalidade de busca de um medicamento por ID.

    Verifica se o método `find` da classe `MedicineFinder` chama corretamente o método
    `select_medicine` do repositório espião e retorna uma resposta com o tipo e atributos
    esperados.
    """
    medicine_id = 1234567890123

    repo = MedicinesRepositorySpy()
    medicine_finder = MedicineFinder(repo)

    response = medicine_finder.find(medicine_id)

    assert repo.select_medicine_attributes["medicine_id"] == medicine_id
    assert response["type"] == "Medicines"
    assert response["attributes"] is not None


def test_find_validation_error_not_integer():
    """Testa a validação de erro quando o ID do medicamento não é um número inteiro.

    Verifica se o método `find` da classe `MedicineFinder` levanta uma exceção `ValueError`
    com a mensagem correta quando o ID fornecido é um número não inteiro.
    """
    medicine_id = 1234567890123.0

    repo = MedicinesRepositorySpy()
    medicine_finder = MedicineFinder(repo)

    try:
        medicine_finder.find(medicine_id)
        assert False, "Expected ValueError not raised"
    except ValueError as e:
        assert str(e) == "O ID do medicamento deve conter apenas números inteiros."


def test_find_validation_error_not_13_digits():
    """Testa a validação de erro quando o ID do medicamento não contém 13 dígitos.

    Verifica se o método `find` da classe `MedicineFinder` levanta uma exceção `ValueError`
    com a mensagem correta quando o ID fornecido não possui exatamente 13 dígitos.
    """
    medicine_id = 12345678901234

    repo = MedicinesRepositorySpy()
    medicine_finder = MedicineFinder(repo)

    try:
        medicine_finder.find(medicine_id)
        assert False, "Expected ValueError not raised"
    except ValueError as e:
        assert str(e) == "O ID do medicamento deve conter 13 dígitos."


def test_find_validation_error_medicine_not_found():
    """Testa a validação de erro quando o medicamento não é encontrado.

    Verifica se o método `find` da classe `MedicineFinder` levanta uma exceção `ValueError`
    com a mensagem correta quando o repositório retorna `None` para o ID fornecido.
    """

    # pylint: disable=C0115:missing-class-docstring
    class MedicinesRepositoryError(MedicinesRepositorySpy):
        def select_medicine(self, medicine_id):
            return None

    medicine_id = 1234567890123

    repo = MedicinesRepositoryError()
    medicine_finder = MedicineFinder(repo)

    try:
        medicine_finder.find(medicine_id)
        assert False, "Expected ValueError not raised"
    except ValueError as e:
        assert str(e) == "Medicamento não encontrado."
