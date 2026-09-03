from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Document, DocumentChunk, DocumentStatus


class DenseRetriever:
    def __init__(self, db: Session):
        self.db = db
    def search(self, tenant_id: str, query_embedding: list[float], top_k: int = 5, distance_threshold: float | None = None, metadata_filters: dict | None = None,):
        conditions = [
            Document.tenant_id == tenant_id,
            Document.status == DocumentStatus.COMPLETED,
        ]

        if metadata_filters:
            for key, value in metadata_filters.items():
                conditions.append(Document.document_metadata[key].as_string() == str(value))

        distance = DocumentChunk.embedding.cosine_distance(query_embedding)
        statement = (
            select(
                DocumentChunk,
                distance.label("distance"),
            )
            .join(Document, Document.id == DocumentChunk.document_id)
            .where(*conditions)
        )

        if distance_threshold is not None:
            statement = statement.where(
                distance <= distance_threshold
            )

        statement = (
            statement
            .order_by(distance)
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