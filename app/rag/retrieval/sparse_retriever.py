from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Document, DocumentChunk, DocumentStatus


class SparseRetriever:
    def __init__(self, db: Session):
        self.db = db

    def search(self, tenant_id: str, query: str, top_k: int = 5, metadata_filters: dict | None = None):
        conditions = [
            Document.tenant_id == tenant_id,
            Document.status == DocumentStatus.COMPLETED,
        ]

        if metadata_filters:
            for key, value in metadata_filters.items():
                conditions.append(
                    Document.document_metadata[key].as_string()
                    == str(value)
                )

        search_query = func.websearch_to_tsquery(
            "english",
            query,
        )

        rank = func.ts_rank(
            DocumentChunk.search_vector,
            search_query,
        )

        statement = (
            select(
                DocumentChunk,
                rank.label("score"),
            )
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .where(
                *conditions,
                DocumentChunk.search_vector.op("@@")(
                    search_query
                ),
            )
            .order_by(rank.desc())
            .limit(top_k)
        )

        results = self.db.execute(statement).all()

        return [
            {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "content": chunk.content,
                "score": float(score),
            }
            for chunk, score in results
        ]