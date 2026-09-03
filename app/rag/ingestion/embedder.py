from dotenv import load_dotenv
from google import genai

load_dotenv()


class Embedder:

    def __init__(self):
        self.client = genai.Client()

    def embed(self, text: str) -> list[float]:
        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
        )

        return response.embeddings[0].values