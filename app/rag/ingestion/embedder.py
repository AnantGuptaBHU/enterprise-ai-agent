from dotenv import load_dotenv
from google.genai import types

load_dotenv()


class Embedder:
    def __init__(self):
        self.client = genai.Client()

    def embed_document(self, text: str) -> list[float]:
        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=3072,
            ),
        )

        return response.embeddings[0].values

    def embed_query(self, text: str) -> list[float]:
        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=3072,
            ),
        )

        return response.embeddings[0].values