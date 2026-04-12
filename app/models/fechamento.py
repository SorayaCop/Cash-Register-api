from datetime import datetime, UTC

from app.extensions import db


class Fechamento(db.Model):
    __tablename__ = "fechamentos"

    id = db.Column(db.Integer, primary_key=True)
    total_entrada = db.Column(db.Numeric(10, 2), nullable=False)
    total_saida = db.Column(db.Numeric(10, 2), nullable=False)
    saldo_esperado = db.Column(db.Numeric(10, 2), nullable=False)
    saldo_informado = db.Column(db.Numeric(10, 2), nullable=False)
    diferenca = db.Column(db.Numeric(10, 2), nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

    def to_dict(self):
        return {
            "id": self.id,
            "total_entrada": float(self.total_entrada),
            "total_saida": float(self.total_saida),
            "saldo_esperado": float(self.saldo_esperado),
            "saldo_informado": float(self.saldo_informado),
            "diferenca": float(self.diferenca),
            "criado_em": self.criado_em.isoformat(),
        }