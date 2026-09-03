from pydantic import BaseModel

from app.db import SessionLocal
from app.rag.generation.generator import Generator
from app.rag.ingestion.embedder import Embedder
from app.rag.retrieval.retriever import Retriever
from app.rag.generation.context_builder import ContextBuilder


class KnowledgeBaseInput(BaseModel):
    query: str
    tenant_id: str


def search_knowledge_base(query: str, tenant_id: str):
    db = SessionLocal()

    try:
        generator = Generator(
            embedder=Embedder(),
            retriever=Retriever(db),
            context_builder=ContextBuilder(),
        )

        return generator.generate(
            user_input=query,
            tenant_id=tenant_id,
        )

    finally:
        db.close()