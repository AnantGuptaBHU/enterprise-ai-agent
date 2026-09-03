from sentence_transformers import CrossEncoder


class Reranker:
    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-base",
    ):
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, results: list[dict], top_k: int = 3) -> list[dict]:
        if not results:
            return []
        pairs = [
            (query, result["content"])
            for result in results
        ]
        scores = self.model.predict(pairs)
        reranked = []
        for result, score in zip(results, scores):
            reranked.append({
                **result,
                "rerank_score": float(score),
            })
        reranked.sort(
            key=lambda result: result["rerank_score"],
            reverse=True,
        )
        return reranked[:top_k]