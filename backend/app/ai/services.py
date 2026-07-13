import logging
from openai import OpenAI
from flask import current_app
from app.extensions import db
from app.ai.models import Conversation, Message

logger = logging.getLogger(__name__)

AVAILABLE_MODELS = [
    {"id": "gpt-4o", "name": "GPT-4o", "description": "Most capable model, best for complex tasks"},
    {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "description": "Fast and efficient, great for everyday tasks"},
    {"id": "gpt-4.1", "name": "GPT-4.1", "description": "Latest generation, improved reasoning"},
    {"id": "gpt-4.1-mini", "name": "GPT-4.1 Mini", "description": "Balanced speed and capability"},
    {"id": "o3", "name": "o3", "description": "Advanced reasoning model"},
    {"id": "o4-mini", "name": "o4-mini", "description": "Fast reasoning model"},
]


def get_client():
    api_key = current_app.config.get("OPENAI_API_KEY")
    return OpenAI(api_key=api_key)


def build_task_context(user_id):
    from app.tasks.models import Task, TaskStatus
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).limit(20).all()
    if not tasks:
        return "The user has no tasks yet."
    lines = []
    for t in tasks:
        status = t.status.value if t.status else "unknown"
        priority = t.priority.value if t.priority else "none"
        due = t.due_date.strftime("%Y-%m-%d") if t.due_date else "no due date"
        lines.append(f"- [{status.upper()}] {t.title} (priority: {priority}, due: {due})")
    return "Current tasks:\n" + "\n".join(lines)


def create_conversation(user_id, model_name="gpt-4o"):
    conv = Conversation(user_id=user_id, model_name=model_name)
    db.session.add(conv)
    db.session.commit()
    return conv


def get_conversation_or_create(user_id, conversation_id=None, model_name="gpt-4o"):
    if conversation_id:
        conv = Conversation.query.filter_by(id=conversation_id, user_id=user_id).first()
        if conv:
            return conv
    return create_conversation(user_id, model_name)


def save_message(conversation_id, role, content, tokens_used=0):
    msg = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        tokens_used=tokens_used,
    )
    db.session.add(msg)
    db.session.commit()
    return msg


def stream_chat(user_id, conversation_id, user_message, model_name=None):
    conv = get_conversation_or_create(user_id, conversation_id, model_name or "gpt-4o")
    if model_name:
        conv.model_name = model_name
        db.session.commit()

    task_context = build_task_context(user_id)

    save_message(conv.id, "user", user_message)

    history = [{"role": "system", "content": f"You are a helpful task management assistant. Help the user manage their tasks efficiently.\n\n{task_context}"}]
    for msg in conv.messages:
        history.append({"role": msg.role, "content": msg.content})

    client = get_client()
    full_response = ""
    try:
        stream = client.chat.completions.create(
            model=conv.model_name,
            messages=history,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                token = chunk.choices[0].delta.content
                full_response += token
                yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"
    except Exception as e:
        logger.error("OpenAI API error: %s", e)
        error_msg = f"AI service error: {str(e)}"
        yield f"data: {error_msg}\n\n"
        yield "data: [DONE]\n\n"
        full_response = error_msg

    save_message(conv.id, "assistant", full_response)

    if conv.title == "New Chat" and len(full_response) > 0:
        conv.title = user_message[:80]
        db.session.commit()


def send_playground_prompt(user_id, model_name, prompt):
    client = get_client()
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content
        tokens = response.usage.total_tokens if response.usage else 0
        return content, tokens
    except Exception as e:
        logger.error("OpenAI playground error: %s", e)
        return None, str(e)
