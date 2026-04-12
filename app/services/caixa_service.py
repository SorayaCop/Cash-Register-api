from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation

from app.errors import ApiError
from app.extensions import db
from app.models.fechamento import Fechamento
from app.models.movimentacao import Movimentacao


def _parse_date(value, field_name):
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ApiError(
            f"The field '{field_name}' must be in YYYY-MM-DD format.",
            400,
            "invalid_date_format",
        )


def _parse_positive_value(value):
    if value is None:
        raise ApiError("The field 'valor' is required.", 400, "missing_field")

    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ApiError("The field 'valor' must be a valid number.", 400, "invalid_value")

    if parsed <= 0:
        raise ApiError("The field 'valor' must be greater than zero.", 400, "invalid_value")

    return parsed


def criar_movimentacao(data):
    tipo = (data.get("tipo") or "").strip().lower()
    forma_pagamento = (data.get("forma_pagamento") or "").strip()
    descricao = (data.get("descricao") or "").strip() or None
    valor = _parse_positive_value(data.get("valor"))

    if tipo not in ["entrada", "saida"]:
        raise ApiError("Invalid 'tipo'. Use 'entrada' or 'saida'.", 400, "invalid_type")

    if not forma_pagamento:
        raise ApiError("The field 'forma_pagamento' is required.", 400, "missing_field")

    mov = Movimentacao(
        tipo=tipo,
        valor=valor,
        forma_pagamento=forma_pagamento,
        descricao=descricao,
    )

    db.session.add(mov)
    db.session.commit()

    return mov.to_dict()


def listar_movimentacoes(data_inicio=None, data_fim=None):
    query = Movimentacao.query

    if data_inicio:
        data_inicio = _parse_date(data_inicio, "data_inicio")
        query = query.filter(Movimentacao.criado_em >= data_inicio)

    if data_fim:
        data_fim = _parse_date(data_fim, "data_fim") + timedelta(days=1)
        query = query.filter(Movimentacao.criado_em < data_fim)

    movimentacoes = query.order_by(Movimentacao.criado_em.desc()).all()

    return [m.to_dict() for m in movimentacoes]


def gerar_resumo_financeiro(data_inicio, data_fim):
    data_inicio = _parse_date(data_inicio, "data_inicio")
    data_fim = _parse_date(data_fim, "data_fim") + timedelta(days=1)

    movimentacoes = Movimentacao.query.filter(
        Movimentacao.criado_em >= data_inicio,
        Movimentacao.criado_em < data_fim
    ).all()

    if not movimentacoes:
        raise ApiError("No data found for this period.", 404, "no_data")

    resumo = {}

    for m in movimentacoes:
        resumo.setdefault(m.forma_pagamento, Decimal("0.00"))

        if m.tipo == "entrada":
            resumo[m.forma_pagamento] += m.valor
        else:
            resumo[m.forma_pagamento] -= m.valor

    total_entrada = sum(
        (m.valor for m in movimentacoes if m.tipo == "entrada"),
        Decimal("0.00")
    )

    total_saida = sum(
        (m.valor for m in movimentacoes if m.tipo == "saida"),
        Decimal("0.00")
    )

    saldo = total_entrada - total_saida

    return {
        "periodo": {
            "inicio": data_inicio.isoformat(),
            "fim": data_fim.isoformat(),
        },
        "total_entrada": float(total_entrada),
        "total_saida": float(total_saida),
        "saldo": float(saldo),
        "resumo_por_forma_pagamento": {
            k: float(v) for k, v in resumo.items()
        },
    }


def calcular_fechamento(saldo_informado, data_inicio, data_fim):
    try:
        saldo_informado = Decimal(str(saldo_informado))
    except:
        raise ApiError("Invalid 'saldo_informado'.", 400, "invalid_value")

    data_inicio = _parse_date(data_inicio, "data_inicio")
    data_fim = _parse_date(data_fim, "data_fim") + timedelta(days=1)

    movimentacoes = Movimentacao.query.filter(
        Movimentacao.criado_em >= data_inicio,
        Movimentacao.criado_em < data_fim
    ).all()

    if not movimentacoes:
        raise ApiError("No transactions found in this period.", 404, "no_data")

    resumo = {}

    for m in movimentacoes:
        resumo.setdefault(m.forma_pagamento, Decimal("0.00"))

        if m.tipo == "entrada":
            resumo[m.forma_pagamento] += m.valor
        else:
            resumo[m.forma_pagamento] -= m.valor

    total_entrada = sum(
        (m.valor for m in movimentacoes if m.tipo == "entrada"),
        Decimal("0.00")
    )

    total_saida = sum(
        (m.valor for m in movimentacoes if m.tipo == "saida"),
        Decimal("0.00")
    )

    saldo_esperado = total_entrada - total_saida
    diferenca = saldo_informado - saldo_esperado

    fechamento = Fechamento(
        total_entrada=total_entrada,
        total_saida=total_saida,
        saldo_esperado=saldo_esperado,
        saldo_informado=saldo_informado,
        diferenca=diferenca,
    )

    db.session.add(fechamento)
    db.session.commit()

    return {
        "id": fechamento.id,
        "periodo": {
            "inicio": data_inicio.isoformat(),
            "fim": data_fim.isoformat(),
        },
        "total_entrada": float(total_entrada),
        "total_saida": float(total_saida),
        "saldo_esperado": float(saldo_esperado),
        "saldo_informado": float(saldo_informado),
        "diferenca": float(diferenca),
        "resumo_por_forma_pagamento": {
            k: float(v) for k, v in resumo.items()
        },
    }


def listar_fechamentos():
    fechamentos = Fechamento.query.order_by(Fechamento.criado_em.desc()).all()
    return [f.to_dict() for f in fechamentos]