from sqlalchemy.orm import Session
from app.models import Conversation, Message, Role

class ConversationService:

    def __init__(self, db: Session):
        self.db = db

    def create_conversation(self, user_id: int) -> Conversation:
        conversation = Conversation(
            user_id=user_id
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_conversation(self, conversation_id: int, user_id: int) -> Conversation | None:
        return (
            self.db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            .first()
        )

    def add_message(self, conversation_id: int, role: Role, content: str | None = None, tool_call_id: str | None = None, tool_name: str | None = None, tool_arguments: dict | None = None) -> Message:
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

    def get_messages(self, conversation_id: int) -> list[Message]:
        return (
            self.db.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .order_by(Message.created_at.asc(), Message.id.asc())
            .all()
        )