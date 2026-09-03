from fastapi import FastAPI

from app.db import Base, engine
from app.models import User, Document, DocumentChunk

from app.routers.document_router import router as document_router
from app.routers.ingestion_router import router as ingestion_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprise AI Agent")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(document_router)
app.include_router(ingestion_router)