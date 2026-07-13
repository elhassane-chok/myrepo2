from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
cors = CORS()


def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    @login_manager.unauthorized_handler
    def unauthorized():
        from flask import jsonify
        return jsonify({"success": False, "message": "Authentication required"}), 401
