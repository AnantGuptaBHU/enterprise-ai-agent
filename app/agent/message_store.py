from app.models import Role
from sqlalchemy.orm import Session
from app.models import Message

class MessageStore:
    def __init__(self, db: Session):
        self.db = db
    def save_message(self, conversation_id: int, role: Role, content: str | None = None, tool_call_id: str | None = None, tool_name: str | None = None, tool_arguments: dict | None = None):
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_call_id=tool_call_id,
            tool_name=tool_name,
            tool_arguments=tool_arguments,
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message