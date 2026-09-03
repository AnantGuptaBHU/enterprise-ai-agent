# from app.db import SessionLocal
# from app.ingestion.embedder import Embedder
# from app.retrieval.retriever import Retriever


# db = SessionLocal()

# embedder = Embedder()
# retriever = Retriever(db)

# query = "What is the warranty policy?"

# query_embedding = embedder.embed(query)

# results = retriever.search(
#     tenant_id="tenant-001",
#     query_embedding=query_embedding,
#     top_k=5,
# )

# for chunk, distance in results:
#     print("\n---")
#     print("Chunk:", chunk.chunk_index)
#     print("Distance:", distance)
#     print("Content:", chunk.content[:300])

# db.close()