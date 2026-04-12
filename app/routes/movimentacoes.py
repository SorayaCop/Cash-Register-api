from flask import Blueprint, request

from app.errors import ApiError, success_response
from app.services.caixa_service import criar_movimentacao, listar_movimentacoes

movimentacoes_bp = Blueprint("movimentacoes", __name__)


@movimentacoes_bp.route("/movimentacoes", methods=["GET"])
def obter_movimentacoes():
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    movimentacoes = listar_movimentacoes(data_inicio, data_fim)

    return success_response(
        data=movimentacoes,
        message="Transactions retrieved successfully.",
        status_code=200,
    )


@movimentacoes_bp.route("/movimentacoes", methods=["POST"])
def adicionar_movimentacao():
    data = request.get_json()

    if not data:
        raise ApiError(
            message="Request body is required.",
            status_code=400,
            error_code="missing_body",
        )

    movimentacao = criar_movimentacao(data)

    return success_response(
        data=movimentacao,
        message="Transaction created successfully.",
        status_code=201,
    )