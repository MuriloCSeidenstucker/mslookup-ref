from typing import Callable, Optional

from fastapi import Request

from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


async def request_adapter(
    request: Request,
    controller: Callable[[HttpRequest], HttpResponse],
) -> HttpResponse:
    body: Optional[dict] = None

    if request.method in {"POST", "PUT", "PATCH"}:
        try:
            body = await request.json()
        except Exception:
            body = None

    http_request = HttpRequest(
        body=body,
        headers=dict(request.headers),
        query_params=dict(request.query_params),
        path_params=request.path_params,
        url=str(request.url),
        ipv4=request.client.host if request.client else None,
    )

    return controller(http_request)
