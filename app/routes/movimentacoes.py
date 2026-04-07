from flask import Blueprint, jsonify, request
from app.services.caixa_service import criar_movimentacao, listar_movimentacoes

movimentacoes_bp = Blueprint("movimentacoes", __name__)


@movimentacoes_bp.route("/movimentacoes", methods=["GET"])
def obter_movimentacoes():
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    movimentacoes = listar_movimentacoes(data_inicio, data_fim)
    return jsonify(movimentacoes)


@movimentacoes_bp.route("/movimentacoes", methods=["POST"])
def adicionar_movimentacao():
    data = request.get_json()

    resultado, status_code = criar_movimentacao(data)

    return jsonify(resultado), status_code