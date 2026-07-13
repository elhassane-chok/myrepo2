from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(exc):
        logger.warning("HTTP %s: %s", exc.code, exc.description)
        return jsonify({
            "success": False,
            "message": exc.description,
        }), exc.code

    @app.errorhandler(Exception)
    def handle_generic_exception(exc):
        logger.error("Unhandled exception: %s", exc, exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error",
        }), 500
