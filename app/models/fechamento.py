from app.extensions import db


class Fechamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_entrada = db.Column(db.Float, nullable=False)
    total_saida = db.Column(db.Float, nullable=False)
    saldo_esperado = db.Column(db.Float, nullable=False)
    saldo_informado = db.Column(db.Float, nullable=False)
    diferenca = db.Column(db.Float, nullable=False)