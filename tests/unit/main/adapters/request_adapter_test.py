from unittest.mock import AsyncMock, MagicMock

import pytest

from src.main.adapters.request_adapter import request_adapter
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


@pytest.mark.anyio
async def test_request_adapter_get():
    mock_request = MagicMock()
    mock_request.method = "GET"
    mock_request.headers = {"user-agent": "test"}
    mock_request.query_params = {"param1": "value1"}
    mock_request.path_params = {"id": "123"}
    mock_request.url = "http://testserver/drugs"
    mock_request.client = MagicMock()
    mock_request.client.host = "127.0.0.1"

    dummy_response = HttpResponse(status_code=200, body={"ok": True})
    controller_called_with = None

    def dummy_controller(http_request: HttpRequest) -> HttpResponse:
        nonlocal controller_called_with
        controller_called_with = http_request
        return dummy_response

    response = await request_adapter(mock_request, dummy_controller)

    assert response == dummy_response
    assert controller_called_with is not None
    assert controller_called_with.body is None
    assert controller_called_with.headers == {"user-agent": "test"}
    assert controller_called_with.query_params == {"param1": "value1"}
    assert controller_called_with.path_params == {"id": "123"}
    assert controller_called_with.url == "http://testserver/drugs"
    assert controller_called_with.ipv4 == "127.0.0.1"


@pytest.mark.anyio
async def test_request_adapter_post_valid_json():
    mock_request = MagicMock()
    mock_request.method = "POST"
    mock_request.json = AsyncMock(return_value={"product_name": "aspirin"})
    mock_request.headers = {}
    mock_request.query_params = {}
    mock_request.path_params = {}
    mock_request.url = "http://testserver/drugs"
    mock_request.client = None

    dummy_response = HttpResponse(status_code=201, body={"created": True})
    controller_called_with = None

    def dummy_controller(http_request: HttpRequest) -> HttpResponse:
        nonlocal controller_called_with
        controller_called_with = http_request
        return dummy_response

    response = await request_adapter(mock_request, dummy_controller)

    assert response == dummy_response
    assert controller_called_with is not None
    assert controller_called_with.body == {"product_name": "aspirin"}
    assert controller_called_with.ipv4 is None


@pytest.mark.anyio
async def test_request_adapter_post_invalid_json():
    mock_request = MagicMock()
    mock_request.method = "POST"
    mock_request.json = AsyncMock(side_effect=Exception("Invalid JSON"))
    mock_request.headers = {}
    mock_request.query_params = {}
    mock_request.path_params = {}
    mock_request.url = "http://testserver/drugs"
    mock_request.client = None

    dummy_response = HttpResponse(status_code=400, body={"error": "bad request"})
    controller_called_with = None

    def dummy_controller(http_request: HttpRequest) -> HttpResponse:
        nonlocal controller_called_with
        controller_called_with = http_request
        return dummy_response

    response = await request_adapter(mock_request, dummy_controller)

    assert response == dummy_response
    assert controller_called_with is not None
    assert controller_called_with.body is None
