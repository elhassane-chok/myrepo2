import logging
import requests
from flask import request, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth_bp
from app.auth.services import create_user, authenticate_email, authenticate_or_create_google
from app.auth.models import User
from app.shared import success_response, error_response

logger = logging.getLogger(__name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return error_response("Request body is required", 400)

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    name = data.get("name", "").strip()

    if not email or not password or not name:
        return error_response("Email, password, and name are required", 400)
    if len(password) < 6:
        return error_response("Password must be at least 6 characters", 400)

    user, err = create_user(email, password, name)
    if err:
        return error_response(err, 409)

    login_user(user)
    return success_response(data=user.to_dict(), message="Registration successful", status=201)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return error_response("Request body is required", 400)

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return error_response("Email and password are required", 400)

    user = authenticate_email(email, password)
    if not user:
        return error_response("Invalid email or password", 401)

    login_user(user)
    return success_response(data=user.to_dict(), message="Login successful")


@auth_bp.route("/google", methods=["POST"])
def google_login():
    data = request.get_json()
    token = data.get("token") if data else None
    if not token:
        return error_response("Google token is required", 400)

    try:
        resp = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
        if resp.status_code != 200:
            return error_response("Invalid Google token", 401)
        info = resp.json()
    except requests.RequestException:
        return error_response("Failed to verify Google token", 502)

    user = authenticate_or_create_google(
        google_id=info["sub"],
        email=info["email"],
        name=info.get("name", info["email"]),
        avatar_url=info.get("picture"),
    )
    login_user(user)
    return success_response(data=user.to_dict(), message="Google login successful")


@auth_bp.route("/me", methods=["GET"])
@login_required
def me():
    return success_response(data=current_user.to_dict())


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return success_response(message="Logged out successfully")
