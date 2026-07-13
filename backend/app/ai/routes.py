import logging
from flask import request, Response, stream_with_context
from flask_login import login_required, current_user
from app.ai import ai_bp
from app.ai.models import Conversation
from app.ai.services import (
    AVAILABLE_MODELS, stream_chat, send_playground_prompt,
    get_conversation_or_create,
)
from app.shared import success_response, error_response

logger = logging.getLogger(__name__)


@ai_bp.route("/models", methods=["GET"])
@login_required
def list_models():
    return success_response(data=AVAILABLE_MODELS)


@ai_bp.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json()
    if not data or not data.get("message"):
        return error_response("Message is required", 400)

    return Response(
        stream_with_context(stream_chat(
            user_id=current_user.id,
            conversation_id=data.get("conversation_id"),
            user_message=data["message"],
            model_name=data.get("model_name"),
        )),
        content_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@ai_bp.route("/conversations", methods=["GET"])
@login_required
def list_conversations():
    convs = Conversation.query.filter_by(user_id=current_user.id).order_by(Conversation.updated_at.desc()).all()
    return success_response(data=[c.to_dict() for c in convs])


@ai_bp.route("/conversations/<conv_id>", methods=["GET"])
@login_required
def get_conversation(conv_id):
    conv = get_conversation_or_create(current_user.id, conv_id)
    return success_response(data=conv.to_dict(include_messages=True))


@ai_bp.route("/conversations/<conv_id>", methods=["DELETE"])
@login_required
def delete_conversation(conv_id):
    conv = Conversation.query.filter_by(id=conv_id, user_id=current_user.id).first()
    if not conv:
        return error_response("Conversation not found", 404)
    from app.extensions import db
    db.session.delete(conv)
    db.session.commit()
    return success_response(message="Conversation deleted")


@ai_bp.route("/playground", methods=["POST"])
@login_required
def playground():
    data = request.get_json()
    if not data or not data.get("prompt"):
        return error_response("Prompt is required", 400)

    model_name = data.get("model_name", "gpt-4o")
    content, tokens = send_playground_prompt(current_user.id, model_name, data["prompt"])

    if content is None:
        return error_response(f"AI error: {tokens}", 502)

    return success_response(data={
        "response": content,
        "tokens_used": tokens,
        "model": model_name,
    })
