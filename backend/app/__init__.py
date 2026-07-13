import os
from flask import Flask

from app.config import config_by_name
from app.extensions import db, migrate, login_manager, init_extensions


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    init_extensions(app)
    _register_blueprints(app)
    _register_error_handlers(app)
    _configure_logging(app)

    @app.route("/api/health")
    def health():
        return {"status": "ok"}

    if config_name == "production":
        _serve_frontend(app)

    return app


def _serve_frontend(app):
    import os
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        from flask import send_from_directory
        if path and os.path.exists(os.path.join(static_dir, path)):
            return send_from_directory(static_dir, path)
        return send_from_directory(static_dir, "index.html")


def _register_blueprints(app):
    from app.auth import auth_bp
    from app.tasks import tasks_bp
    from app.ai import ai_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(tasks_bp, url_prefix="/api")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")


def _register_error_handlers(app):
    from app.shared.errors import register_error_handlers
    register_error_handlers(app)


def _configure_logging(app):
    from app.shared.logging_config import setup_async_logging
    setup_async_logging(app)
