# pylint: disable=W0718:broad-exception-caught

import uuid

from fastapi import APIRouter, Request

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


@router.get("/search")
async def search_drugs(request: Request):
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
        len(http_response.body.get("data", [])),
        log_id,
    )

    return http_response.body
