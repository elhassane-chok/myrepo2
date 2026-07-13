from flask import jsonify


def success_response(data=None, message="", status=200):
    payload = {"success": True, "message": message}
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status


def error_response(message="An error occurred", status=400, errors=None):
    payload = {"success": False, "message": message}
    if errors:
        payload["errors"] = errors
    return jsonify(payload), status
