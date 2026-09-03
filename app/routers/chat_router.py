from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.agent.message_store import MessageStore
from app.agent.agent import Agent
from app.db import get_db
from app.models import Role
from app.services.conversation_service import ConversationService

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)

class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None
class ChatResponse(BaseModel):
    message: str
    conversation_id: int

@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    conversation_service = ConversationService(db)
    message_store = MessageStore(db)
    # Temporary user until authentication is implemented##########################################?????????
    user_id = 1
    if request.conversation_id is None:
        conversation = conversation_service.create_conversation(user_id = user_id)
    else:
        conversation = conversation_service.get_conversation(conversation_id=request.conversation_id, user_id=user_id)
        if conversation is None:
            raise ValueError("Conversation not found")
    message_store.save_message(conversation_id=conversation.id, role=Role.USER, content=request.message)
    # conversation_service.add_message(conversation_id=conversation.id, role=Role.USER, content=request.message)
    agent = Agent(message_store=message_store)
    result = agent.run(request.message, conversation_id=conversation.id)
    if not result.success:
        raise RuntimeError(result.error)
    # conversation_service.add_message(conversation_id=conversation.id, role=Role.ASSISTANT, content=result.output)
    message_store.save_message(conversation_id=conversation.id, role=Role.ASSISTANT, content=result.output)
    return ChatResponse(
        conversation_id=conversation.id,
        message=result.output,
    )