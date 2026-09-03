from app.rag.ingestion.embedder import Embedder
from app.rag.retrieval.retriever import Retriever
from app.rag.generation.context_builder import ContextBuilder


class Generator:

    def __init__(self, embedder: Embedder, retriever: Retriever, context_builder: ContextBuilder):
        self.embedder = embedder
        self.retriever = retriever
        self.context_builder = context_builder

    def generate(self, user_input: str, tenant_id: str, top_k: int = 5) -> str:

        query_embedding = self.embedder.embed_query(user_input)

        results = self.retriever.search(
            tenant_id=tenant_id,
            query=user_input,
            query_embedding=query_embedding,
            top_k=top_k,
            distance_threshold=0.4,
        )
        context = self.context_builder.build(results)
        print("context is ----- ",context)
        return context