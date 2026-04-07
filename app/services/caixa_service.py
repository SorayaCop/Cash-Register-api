from app.extensions import db
from app.models.movimentacao import Movimentacao
from app.models.fechamento import Fechamento


def criar_movimentacao(data):
    tipo = data.get("tipo")
    valor = data.get("valor")
    forma_pagamento = data.get("forma_pagamento")

    if not tipo:
        return {"erro": "O campo 'tipo' é obrigatório."}, 400

    if tipo not in ["entrada", "saida"]:
        return {"erro": "O campo 'tipo' deve ser 'entrada' ou 'saida'."}, 400

    if valor is None:
        return {"erro": "O campo 'valor' é obrigatório."}, 400

    if valor <= 0:
        return {"erro": "O campo 'valor' deve ser maior que zero."}, 400

    if not forma_pagamento:
        return {"erro": "O campo 'forma_pagamento' é obrigatório."}, 400

    movimentacao = Movimentacao(
        tipo=tipo,
        valor=valor,
        forma_pagamento=forma_pagamento
    )

    db.session.add(movimentacao)
    db.session.commit()

    return {
        "id": movimentacao.id,
        "tipo": movimentacao.tipo,
        "valor": movimentacao.valor,
        "forma_pagamento": movimentacao.forma_pagamento,
        "criado_em": movimentacao.criado_em.isoformat()
    }, 201


def listar_movimentacoes():
    movimentacoes = Movimentacao.query.all()

    return [
        {
            "id": movimentacao.id,
            "tipo": movimentacao.tipo,
            "valor": movimentacao.valor,
            "forma_pagamento": movimentacao.forma_pagamento,
            "criado_em": movimentacao.criado_em.isoformat()
        }
        for movimentacao in movimentacoes
    ]


def calcular_fechamento(saldo_informado):
    movimentacoes = Movimentacao.query.all()

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
        diferenca=diferenca
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
        "criado_em": fechamento.criado_em.isoformat()
    }


def listar_fechamentos():
    fechamentos = Fechamento.query.all()

    return [
        {
            "id": f.id,
            "total_entrada": f.total_entrada,
            "total_saida": f.total_saida,
            "saldo_esperado": f.saldo_esperado,
            "saldo_informado": f.saldo_informado,
            "diferenca": f.diferenca,
            "criado_em": f.criado_em.isoformat()
        }
        for f in fechamentos
    ]