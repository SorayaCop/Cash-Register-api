from flask import Blueprint, jsonify, request
from app.services.caixa_service import calcular_fechamento, listar_fechamentos

fechamentos_bp = Blueprint("fechamentos", __name__)


@fechamentos_bp.route("/fechamentos", methods=["POST"])
def fechar_caixa():
    data = request.get_json()

    saldo_informado = data.get("saldo_informado")

    if saldo_informado is None:
        return jsonify({"erro": "O campo 'saldo_informado' é obrigatório."}), 400

    fechamento = calcular_fechamento(saldo_informado)

    return jsonify(fechamento), 200


@fechamentos_bp.route("/fechamentos", methods=["GET"])
def obter_fechamentos():
    fechamentos = listar_fechamentos()
    return jsonify(fechamentos)