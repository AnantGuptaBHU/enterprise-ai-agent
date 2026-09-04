from app.agent.agent import Agent
from app.db import SessionLocal
from app.agent.message_store import MessageStore

db = SessionLocal()
try:
    message_store = MessageStore(db)
    agent = Agent(message_store=message_store)

    result = agent.run("What is the warranty period of mobile phone?",conversation_id=1,)

    print(result)
finally:
    db.close()
