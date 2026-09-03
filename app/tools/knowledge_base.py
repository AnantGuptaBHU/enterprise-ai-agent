from pydantic import BaseModel


class KnowledgeBaseInput(BaseModel):
    query: str


def search_knowledge_base(query: str):

    return {
        "query": query,
        "results": [
            {
                "title": "Refund Policy",
                "content": "Customers can request a refund within 30 days."
            },
            {
                "title": "Support Policy",
                "content": "Customer support is available Monday to Friday."
            }
        ]
    }