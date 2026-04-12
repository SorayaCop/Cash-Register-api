from datetime import datetime, UTC

from app.extensions import db


class Movimentacao(db.Model):
    __tablename__ = "movimentacoes"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "valor": float(self.valor),
            "forma_pagamento": self.forma_pagamento,
            "descricao": self.descricao,
            "criado_em": self.criado_em.isoformat(),
        }