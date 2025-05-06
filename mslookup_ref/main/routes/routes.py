from flask import Blueprint, jsonify, request

from mslookup_ref.main.adapters.request_adapter import request_adapter
from mslookup_ref.main.composers.medicine_finder_composer import (
    medicine_finder_composer,
)
from mslookup_ref.main.composers.medicine_register_composer import (
    medicine_register_composer,
)

medicine_route_bp = Blueprint("medicine_routes", __name__)


@medicine_route_bp.route("/medicine/find", methods=["GET"])
def find_medicine():
    """Rota para buscar um medicamento por ID.

    Processa uma requisição GET com um parâmetro de consulta 'medicine_id', utiliza o
    adaptador para converter a requisição Flask em um HttpRequest e invoca o controlador
    composto por medicine_finder_composer para realizar a busca. Retorna os dados do
    medicamento em formato JSON.

    Returns:
        tuple: Par contendo o corpo da resposta em JSON (dicionário com os dados do
            medicamento) e o código de status HTTP.

    Example:
        GET /medicine/find?medicine_id=1234567890123
        Response: {"data": {"type": "Medicines", "attributes": {...}}}, 200
    """

    http_response = request_adapter(request, medicine_finder_composer())
    return jsonify(http_response.body), http_response.status_code


@medicine_route_bp.route("/medicine", methods=["POST"])
def register_medicine():
    """Rota para registrar um medicamento.

    Processa uma requisição POST com um corpo JSON contendo os dados do medicamento,
    utiliza o adaptador para converter a requisição Flask em um HttpRequest e invoca o
    controlador composto por medicine_register_composer para realizar o registro. Retorna
    os dados registrados em formato JSON.

    Returns:
        tuple: Par contendo o corpo da resposta em JSON (dicionário com os dados registrados)
            e o código de status HTTP.

    Example:
        POST /medicine
        Body: {"medicine": {"id": 1234567890123, "product": "product1", ...}}
        Response: {"data": {"type": "Medicines", "attributes": {...}}}, 200
    """

    http_response = request_adapter(request, medicine_register_composer())
    return jsonify(http_response.body), http_response.status_code
