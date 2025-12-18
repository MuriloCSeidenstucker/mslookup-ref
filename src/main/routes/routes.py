# pylint: disable=W0718:broad-exception-caught

import uuid

from flask import Blueprint, g, jsonify, request

from src.errors.error_handler import handle_errors
from src.logging import LevelName, LoggerHandler
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.medicine_finder_composer import medicine_finder_composer
from src.main.composers.medicine_register_composer import medicine_register_composer
from src.validators.medicine_finder_validator import medicine_finder_validator
from src.validators.medicine_register_validator import medicine_register_validator

logger_handler = LoggerHandler(LevelName.DEBUG)
logger = logger_handler.get_logger()

medicine_route_bp = Blueprint("medicine_routes", __name__)


@medicine_route_bp.route("/medicine/find", methods=["GET"])
def find_medicine():
    """Rota para buscar um medicamento por ID.

    Processa uma requisição GET com um parâmetro de consulta 'medicine_id', converte a
    requisição Flask em um HttpRequest usando o adaptador e invoca o controlador composto
    por medicine_finder_composer para realizar a busca. Retorna os dados do medicamento
    em formato JSON ou uma resposta de erro padronizada, se aplicável.

    Returns:
        tuple: Par contendo o corpo da resposta em JSON (dicionário com os dados do
            medicamento ou mensagem de erro) e o código de status HTTP.

    Raises:
        HttpBadRequestError: Se o parâmetro 'medicine_id' estiver ausente ou inválido.
        HttpNotFoundError: Se o medicamento não for encontrado.
        Exception: Outros erros inesperados são tratados como erro interno (status 500).

    Examples:
        GET /medicine/find?medicine_id=1234567890123
        Response: {"data": {"type": "Medicines", "attributes": {...}}}, 200
    """

    http_response = None
    g.log_id = str(uuid.uuid4())

    try:
        logger.info(
            "Iniciando busca de medicamento: endpoint=/medicine/find, method=GET, params=%s",
            request.args,
        )
        medicine_finder_validator(request)
        http_response = request_adapter(request, medicine_finder_composer())
        logger.info(
            "Busca concluída: status_code=%s, response_body=%s",
            http_response.status_code,
            http_response.body,
        )
    except Exception as e:
        logger.error(
            "Erro ao processar busca de medicamento: error_type=%s, message=%s",
            type(e).__name__,
            str(e),
            exc_info=True,
        )
        http_response = handle_errors(e)

    return jsonify(http_response.body), http_response.status_code


@medicine_route_bp.route("/medicine", methods=["POST"])
def register_medicine():
    """Rota para registrar um medicamento.

    Processa uma requisição POST com um corpo JSON contendo os dados do medicamento,
    converte a requisição Flask em um HttpRequest usando o adaptador e invoca o controlador
    composto por medicine_register_composer para realizar o registro. Retorna os dados
    registrados em formato JSON ou uma resposta de erro padronizada, se aplicável.

    Returns:
        tuple: Par contendo o corpo da resposta em JSON (dicionário com os dados registrados
            ou mensagem de erro) e o código de status HTTP.

    Raises:
        HttpBadRequestError: Se os dados do medicamento estiverem ausentes ou inválidos.
        Exception: Outros erros inesperados são tratados como erro interno (status 500).

    Examples:
        POST /medicine
        Body: {"medicine": {"id": 1234567890123, "product": "product1", ...}}
        Response: {"data": {"type": "Medicines", "attributes": {...}}}, 200
    """

    http_response = None
    g.log_id = str(uuid.uuid4())

    try:
        logger.info(
            "Iniciando registro de medicamento: endpoint=/medicine, method=POST, body=%s",
            request.get_json(),
        )
        medicine_register_validator(request)
        http_response = request_adapter(request, medicine_register_composer())
        logger.info(
            "Registro concluído: status_code=%s, response_body=%s",
            http_response.status_code,
            http_response.body,
        )
    except Exception as e:
        logger.error(
            "Erro ao processar registro de medicamento: error_type=%s, message=%s",
            type(e).__name__,
            str(e),
            exc_info=True,
        )
        http_response = handle_errors(e)

    return jsonify(http_response.body), http_response.status_code
