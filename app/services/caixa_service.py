from datetime import datetime, timedelta

from app.errors import ApiError
from app.extensions import db
from app.models.fechamento import Fechamento
from app.models.movimentacao import Movimentacao


def _parse_date(value, field_name):
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ApiError(
            message=f"The field '{field_name}' must be in YYYY-MM-DD format.",
            status_code=400,
            error_code="invalid_date_format",
        )


def _parse_positive_value(value):
    if value is None:
        raise ApiError(
            message="The field 'valor' is required.",
            status_code=400,
            error_code="missing_field",
        )

    try:
        parsed_value = float(value)
    except (TypeError, ValueError):
        raise ApiError(
            message="The field 'valor' must be a valid number.",
            status_code=400,
            error_code="invalid_value",
        )

    if parsed_value <= 0:
        raise ApiError(
            message="The field 'valor' must be greater than zero.",
            status_code=400,
            error_code="invalid_value",
        )

    return parsed_value


def criar_movimentacao(data):
    tipo = (data.get("tipo") or "").strip().lower()
    forma_pagamento = (data.get("forma_pagamento") or "").strip()
    descricao = (data.get("descricao") or "").strip() or None
    valor = _parse_positive_value(data.get("valor"))

    if not tipo:
        raise ApiError(
            message="The field 'tipo' is required.",
            status_code=400,
            error_code="missing_field",
        )

    if tipo not in ["entrada", "saida"]:
        raise ApiError(
            message="The field 'tipo' must be 'entrada' or 'saida'.",
            status_code=400,
            error_code="invalid_type",
        )

    if not forma_pagamento:
        raise ApiError(
            message="The field 'forma_pagamento' is required.",
            status_code=400,
            error_code="missing_field",
        )

    movimentacao = Movimentacao(
        tipo=tipo,
        valor=valor,
        forma_pagamento=forma_pagamento,
        descricao=descricao,
    )

    db.session.add(movimentacao)
    db.session.commit()

    return {
        "id": movimentacao.id,
        "tipo": movimentacao.tipo,
        "valor": movimentacao.valor,
        "forma_pagamento": movimentacao.forma_pagamento,
        "descricao": movimentacao.descricao,
        "criado_em": movimentacao.criado_em.isoformat(),
    }


def listar_movimentacoes(data_inicio=None, data_fim=None):
    query = Movimentacao.query

    if data_inicio:
        data_inicio_obj = _parse_date(data_inicio, "data_inicio")
        query = query.filter(Movimentacao.criado_em >= data_inicio_obj)

    if data_fim:
        data_fim_obj = _parse_date(data_fim, "data_fim") + timedelta(days=1)
        query = query.filter(Movimentacao.criado_em < data_fim_obj)

    if data_inicio and data_fim and data_inicio_obj > data_fim_obj - timedelta(days=1):
        raise ApiError(
            message="'data_inicio' cannot be greater than 'data_fim'.",
            status_code=400,
            error_code="invalid_date_range",
        )

    movimentacoes = query.order_by(Movimentacao.criado_em.desc()).all()

    return [
        {
            "id": movimentacao.id,
            "tipo": movimentacao.tipo,
            "valor": movimentacao.valor,
            "forma_pagamento": movimentacao.forma_pagamento,
            "descricao": movimentacao.descricao,
            "criado_em": movimentacao.criado_em.isoformat(),
        }
        for movimentacao in movimentacoes
    ]


def calcular_fechamento(saldo_informado):
    movimentacoes = Movimentacao.query.all()
    resumo_por_forma_pagamento = {}

    for movimentacao in movimentacoes:
        forma = movimentacao.forma_pagamento

        if forma not in resumo_por_forma_pagamento:
            resumo_por_forma_pagamento[forma] = 0

        if movimentacao.tipo == "entrada":
            resumo_por_forma_pagamento[forma] += movimentacao.valor
        else:
            resumo_por_forma_pagamento[forma] -= movimentacao.valor

    total_entrada = sum(
        movimentacao.valor
        for movimentacao in movimentacoes
        if movimentacao.tipo == "entrada"
    )

    total_saida = sum(
        movimentacao.valor
        for movimentacao in movimentacoes
        if movimentacao.tipo == "saida"
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
        "total_entrada": fechamento.total_entrada,
        "total_saida": fechamento.total_saida,
        "saldo_esperado": fechamento.saldo_esperado,
        "saldo_informado": fechamento.saldo_informado,
        "diferenca": fechamento.diferenca,
        "criado_em": fechamento.criado_em.isoformat(),
        "resumo_por_forma_pagamento": resumo_por_forma_pagamento,
    }


def listar_fechamentos():
    fechamentos = Fechamento.query.order_by(Fechamento.criado_em.desc()).all()

    return [
        {
            "id": f.id,
            "total_entrada": f.total_entrada,
            "total_saida": f.total_saida,
            "saldo_esperado": f.saldo_esperado,
            "saldo_informado": f.saldo_informado,
            "diferenca": f.diferenca,
            "criado_em": f.criado_em.isoformat(),
        }
        for f in fechamentos
    ]