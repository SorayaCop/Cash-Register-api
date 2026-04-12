from flask import Blueprint, request

from app.errors import ApiError, success_response
from app.services.caixa_service import calcular_fechamento, listar_fechamentos

fechamentos_bp = Blueprint("fechamentos", __name__)


@fechamentos_bp.route("/fechamentos", methods=["POST"])
def fechar_caixa():
    data = request.get_json(silent=True)

    if not data:
        raise ApiError(
            message="Request body is required.",
            status_code=400,
            error_code="missing_body",
        )

    saldo_informado = data.get("saldo_informado")
    data_inicio = data.get("data_inicio")
    data_fim = data.get("data_fim")

    if saldo_informado is None:
        raise ApiError(
            message="The field 'saldo_informado' is required.",
            status_code=400,
            error_code="missing_field",
        )

    if not data_inicio or not data_fim:
        raise ApiError(
            message="Fields 'data_inicio' and 'data_fim' are required.",
            status_code=400,
            error_code="missing_field",
        )

    fechamento = calcular_fechamento(
        saldo_informado=saldo_informado,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )

    return success_response(
        data=fechamento,
        message="Cash closing calculated successfully.",
        status_code=200,
    )


@fechamentos_bp.route("/fechamentos", methods=["GET"])
def obter_fechamentos():
    fechamentos = listar_fechamentos()

    return success_response(
        data=fechamentos,
        message="Cash closings retrieved successfully.",
        status_code=200,
    )