from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Document, DocumentChunk, DocumentStatus


class Retriever:
    def __init__(self, db: Session):
        self.db = db
    def search(self, tenant_id: str, query_embedding: list[float], top_k: int = 5):
        statement = (
            select(
                DocumentChunk,
                DocumentChunk.embedding.cosine_distance(
                    query_embedding
                ).label("distance"),
            )
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .where(
                Document.tenant_id == tenant_id,
                Document.status == DocumentStatus.COMPLETED,
            )
            .order_by("distance")
            .limit(top_k)
        )

        results = self.db.execute(statement).all()

        return [
            {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "content": chunk.content,
                "distance": float(distance),
            }
            for chunk, distance in results
        ]