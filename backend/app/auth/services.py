import logging
from app.extensions import db
from app.auth.models import User

logger = logging.getLogger(__name__)


def create_user(email, password, name):
    existing = User.query.filter_by(email=email).first()
    if existing:
        return None, "Email already registered"
    user = User(email=email, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    logger.info("User registered: %s", user.email)
    return user, None


def authenticate_email(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return None
    logger.info("User logged in: %s", user.email)
    return user


def authenticate_or_create_google(google_id, email, name, avatar_url=None):
    user = User.query.filter_by(google_id=google_id).first()
    if user:
        return user
    user = User.query.filter_by(email=email).first()
    if user:
        user.google_id = google_id
        if avatar_url:
            user.avatar_url = avatar_url
        db.session.commit()
        logger.info("Google account linked: %s", user.email)
        return user
    user = User(
        email=email,
        name=name,
        google_id=google_id,
        avatar_url=avatar_url,
    )
    db.session.add(user)
    db.session.commit()
    logger.info("User created via Google: %s", user.email)
    return user
