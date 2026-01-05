from unittest.mock import Mock

import pytest

from src.presentation.controllers.drug_finder_controller import DrugFinderController
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

# =========================
# Fixtures
# =========================


@pytest.fixture
def use_case_mock():
    return Mock()


@pytest.fixture
def controller(use_case_mock):
    return DrugFinderController(use_case=use_case_mock)


@pytest.fixture
def http_request_with_params():
    return HttpRequest(
        query_params={
            "product_name": " Dipirona ",
            "active_ingredient": " Dipirona Monoidratada ",
            "registration_holder": " Empresa X ",
        }
    )


# =========================
# Caminho feliz
# =========================


def test_handle_returns_http_response_success(
    controller,
    use_case_mock,
    http_request_with_params,
    mocker,
):
    # Arrange
    mocker.patch(
        "src.presentation.controllers.drug_finder_controller.normalize_text",
        side_effect=lambda x: x.strip().lower() if x else None,
    )

    expected_use_case_response = {
        "type": "DrugRegistrations",
        "count": 1,
        "attributes": [],
    }

    use_case_mock.find.return_value = expected_use_case_response

    # Act
    response = controller.handle(http_request_with_params)

    # Assert
    assert isinstance(response, HttpResponse)
    assert response.status_code == 200
    assert response.body == {"data": expected_use_case_response}

    use_case_mock.find.assert_called_once_with(
        product_name="dipirona",
        active_ingredient="dipirona monoidratada",
        registration_holder="empresa x",
    )


# =========================
# Query params ausentes
# =========================


def test_handle_handles_missing_query_params(controller, use_case_mock, mocker):
    # Arrange
    mocker.patch(
        "src.presentation.controllers.drug_finder_controller.normalize_text",
        return_value=None,
    )

    request = HttpRequest(query_params=None)

    use_case_mock.find.return_value = {"count": 0}

    # Act
    response = controller.handle(request)

    # Assert
    assert response.status_code == 200

    use_case_mock.find.assert_called_once_with(
        product_name=None,
        active_ingredient=None,
        registration_holder=None,
    )


# =========================
# Normalização aplicada
# =========================


def test_handle_calls_normalize_text_for_each_param(
    controller,
    use_case_mock,
    http_request_with_params,
    mocker,
):
    # Arrange
    normalize_mock = mocker.patch(
        "src.presentation.controllers.drug_finder_controller.normalize_text",
        side_effect=["product_name", "ingredient", "holder"],
    )

    use_case_mock.find.return_value = {}

    # Act
    controller.handle(http_request_with_params)

    # Assert
    assert normalize_mock.call_count == 3
    normalize_mock.assert_any_call(" Dipirona ")
    normalize_mock.assert_any_call(" Dipirona Monoidratada ")
    normalize_mock.assert_any_call(" Empresa X ")


# =========================
# Contrato do controller
# =========================


def test_handle_does_not_catch_use_case_exceptions(
    controller,
    use_case_mock,
    http_request_with_params,
    mocker,
):
    # Arrange
    mocker.patch(
        "src.presentation.controllers.drug_finder_controller.normalize_text",
        return_value="dipirona",
    )

    use_case_mock.find.side_effect = Exception("Use case error")

    # Act / Assert
    with pytest.raises(Exception):
        controller.handle(http_request_with_params)
