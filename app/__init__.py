from flask import Flask
from werkzeug.exceptions import BadRequest

from app.config import Config
from app.errors import ApiError, error_response
from app.extensions import db
from app.routes.fechamentos import fechamentos_bp
from app.routes.movimentacoes import movimentacoes_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.models.fechamento import Fechamento
    from app.models.movimentacao import Movimentacao

    @app.get("/")
    def home():
        return {
            "message": "Cash Register API is running!",
            "version": "v1",
            "docs_status": "pending"
        }, 200

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "service": "cash-register-api"
        }, 200

    @app.errorhandler(ApiError)
    def handle_api_error(error):
        return error_response(
            message=error.message,
            status_code=error.status_code,
            error_code=error.error_code,
        )

    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        return error_response(
            message="Invalid JSON payload.",
            status_code=400,
            error_code="invalid_json",
        )

    @app.errorhandler(404)
    def handle_not_found(error):
        return error_response(
            message="Resource not found.",
            status_code=404,
            error_code="not_found",
        )

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return error_response(
            message="Method not allowed for this endpoint.",
            status_code=405,
            error_code="method_not_allowed",
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        return error_response(
            message="Internal server error.",
            status_code=500,
            error_code="internal_server_error",
        )

    app.register_blueprint(movimentacoes_bp, url_prefix="/api/v1")
    app.register_blueprint(fechamentos_bp, url_prefix="/api/v1")

    return app