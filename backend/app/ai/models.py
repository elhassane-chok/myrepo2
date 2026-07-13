import uuid
from datetime import datetime, timezone
from app.extensions import db


class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False, default="New Chat")
    model_name = db.Column(db.String(100), nullable=False, default="gpt-4o")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    messages = db.relationship("Message", backref="conversation", lazy=True, cascade="all, delete-orphan",
                               order_by="Message.created_at")

    def to_dict(self, include_messages=False):
        data = {
            "id": self.id,
            "title": self.title,
            "model_name": self.model_name,
            "message_count": len(self.messages),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_messages:
            data["messages"] = [m.to_dict() for m in self.messages]
        return data


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = db.Column(db.String(36), db.ForeignKey("conversations.id"), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tokens_used = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "tokens_used": self.tokens_used,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
