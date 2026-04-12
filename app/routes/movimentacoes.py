from flask import Blueprint, request

from app.errors import ApiError, success_response
from app.services.caixa_service import (
    criar_movimentacao,
    listar_movimentacoes,
    gerar_resumo_financeiro,
)

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
    data = request.get_json(silent=True)

    if not data:
        raise ApiError("Request body is required.", 400, "missing_body")

    movimentacao = criar_movimentacao(data)

    return success_response(
        data=movimentacao,
        message="Transaction created successfully.",
        status_code=201,
    )


@movimentacoes_bp.route("/resumo", methods=["GET"])
def obter_resumo():
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    if not data_inicio or not data_fim:
        raise ApiError(
            "Query params 'data_inicio' and 'data_fim' are required.",
            400,
            "missing_params",
        )

    resumo = gerar_resumo_financeiro(data_inicio, data_fim)

    return success_response(
        data=resumo,
        message="Financial summary retrieved successfully.",
        status_code=200,
    )