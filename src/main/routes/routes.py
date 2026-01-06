# pylint: disable=W0718:broad-exception-caught, W0613:unused-argument

import uuid

from fastapi import APIRouter, Query, Request

from src.logging.logger_handler import LevelName, LoggerHandler
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.drug_finder_composer import drug_finder_composer
from src.validators.drug_finder_validator import drug_finder_validator

logger_handler = LoggerHandler(LevelName.DEBUG)
logger = logger_handler.get_logger()

router = APIRouter(
    prefix="/drugs",
    tags=["Drugs"],
)


@router.get(
    "/search",
    summary="Buscar registros de medicamentos",
    description=(
        "Realiza a busca de registros de medicamentos a partir de dados públicos da ANVISA.\n\n"
        "⚠️ **Aviso importante**:\n"
        "- Os dados retornados são baseados em dados abertos da ANVISA.\n"
        "- A situação regulatória final deve ser confirmada no site oficial da ANVISA.\n"
        "- Este endpoint não substitui a consulta oficial."
    ),
    responses={
        200: {
            "description": "Busca realizada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "data": {
                            "count": 1,
                            "attributes": [
                                {
                                    "registration_number": "123456789",
                                    "product_name": "METRONIDAZOL",
                                    "active_ingredient": "METRONIDAZOL",
                                    "registration_holder": "LABORATÓRIO EXEMPLO",
                                    "expiration_date": "2026-03-01",
                                }
                            ],
                        }
                    }
                }
            },
        },
        404: {
            "description": "Nenhum registro encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "errors": [
                            {
                                "title": "NotFound",
                                "detail": "Nenhum registro ANVISA encontrado.",
                            }
                        ]
                    }
                }
            },
        },
        422: {
            "description": "Parâmetros inválidos",
            "content": {
                "application/json": {
                    "example": {
                        "errors": [
                            {
                                "title": "UnprocessableEntity",
                                "detail": {
                                    "product_name": ["required field"],
                                },
                            }
                        ]
                    }
                }
            },
        },
    },
)
async def search_drugs(
    request: Request,
    product_name: str = Query(
        ...,
        description="Nome comercial do medicamento ou parte dele.",
    ),
    active_ingredient: str | None = Query(
        None,
        description="Princípio ativo do medicamento.",
    ),
    registration_holder: str | None = Query(
        None,
        description="Empresa detentora do registro",
    ),
):
    log_id = str(uuid.uuid4())

    logger.info(
        "Starting drug search: endpoint=/drugs/search, method=GET, params=%s, log_id=%s",
        dict(request.query_params),
        log_id,
    )

    drug_finder_validator(request)

    http_response = await request_adapter(
        request,
        drug_finder_composer(),
    )

    logger.info(
        "Drug search completed: status_code=%s, results=%s, log_id=%s",
        http_response.status_code,
        http_response.body.get("data", {}).get("count", 0),
        log_id,
    )

    return http_response.body
