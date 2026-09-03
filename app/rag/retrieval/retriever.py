from app.rag.retrieval.dense_retriever import DenseRetriever
from app.rag.retrieval.sparse_retriever import SparseRetriever
from sqlalchemy.orm import Session

class Retriever:
    def __init__(self, db: Session):
        self.dense = DenseRetriever(db)
        self.sparse = SparseRetriever(db)

    def search(self, tenant_id: str, query: str, query_embedding: list[float], top_k: int = 5, distance_threshold: float | None = None, metadata_filters: dict | None = None,):
        dense_results = self.dense.search(tenant_id=tenant_id, query_embedding=query_embedding, top_k=top_k, distance_threshold=distance_threshold, metadata_filters=metadata_filters)
        sparse_results = self.sparse.search(tenant_id=tenant_id, query=query, top_k=top_k, metadata_filters=metadata_filters)
        return self._rrf(dense_results, sparse_results, top_k)
    
    def _rrf(self, dense_results: list[dict], sparse_results: list[dict], top_k: int, k: int = 60):
        scores = {}
        chunks = {}
        for rank, result in enumerate(dense_results, start=1):
            chunk_id = result["chunk_id"]
            scores[chunk_id] = scores.get(chunk_id, 0) + (
                1 / (k + rank)
            )
            chunks[chunk_id] = result

        for rank, result in enumerate(sparse_results, start=1):
            chunk_id = result["chunk_id"]
            scores[chunk_id] = scores.get(chunk_id, 0) + (
                1 / (k + rank)
            )
            chunks[chunk_id] = result
        ranked = sorted(
            scores,
            key=scores.get,
            reverse=True,
        )
        return [
            {
                **chunks[chunk_id],
                "rrf_score": scores[chunk_id],
            }
            for chunk_id in ranked[:top_k]
        ]