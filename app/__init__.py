from flask import Flask
from app.routes.movimentacoes import movimentacoes_bp
from app.routes.fechamentos import fechamentos_bp
from app.extensions import db


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.models.movimentacao import Movimentacao
    from app.models.fechamento import Fechamento

    @app.route("/")
    def home():
        return {"message": "Cash Register API is running!"}

    app.register_blueprint(movimentacoes_bp)
    app.register_blueprint(fechamentos_bp)

    return app