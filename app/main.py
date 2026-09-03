from fastapi import FastAPI

from app.agent.agent import Agent
from app.tools.register import create_tool_registry

from app.db import Base, engine
from app.models import User, Document, DocumentChunk

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprise AI Agent")

tool_registry = create_tool_registry()
# agent = Agent()
# print(agent.run("please mail me the result of 6+7 at anant.vara@gmail.com"))

@app.get("/health")
def health():
    return {"status": "ok"}

from app.routers.document_router import router as document_router
app.include_router(document_router)
from app.routers.ingestion_router import router as ingestion_router
app.include_router(ingestion_router)
