from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_db
from app.models import Document, DocumentChunk, DocumentStatus
from app.schema import IngestionRequest
from app.storage.local import LocalStorage
from app.rag.ingestion.parser import PDFParser
from app.rag.ingestion.chunker import TextChunker
from app.rag.ingestion.embedder import Embedder

router = APIRouter(
    prefix="/ingestion",
    tags=["ingestion"],
)

storage = LocalStorage()
parser = PDFParser()
chunker = TextChunker()
embedder = Embedder()


@router.post("/ingest")
async def ingest_document(request: IngestionRequest, db: Session = Depends(get_db),):
    document = Document(
        tenant_id=request.tenant_id,
        filename=request.filename,
        status=DocumentStatus.PROCESSING,
        storage_key=request.storage_key,
        document_metadata=request.metadata,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    try:
        # 1. Read + parse document
        file_path = storage.base_path / request.storage_key
        text = parser.parse(str(file_path))
        # 2. Chunk
        chunks = chunker.chunk(text)
        # 3. Generate embeddings + persist chunks
        for index, chunk_text in enumerate(chunks):
            embedding = embedder.embed_document(chunk_text)
            chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk_text,
                embedding=embedding,
                search_vector=func.to_tsvector("english", chunk_text),
                document_metadataa=request.metadata,
            )
            db.add(chunk)
        # 4. Mark document completed
        document.status = DocumentStatus.COMPLETED
        db.commit()
        return {
            "document_id": document.id,
            "status": document.status,
            "chunks_created": len(chunks),
        }

    except Exception as e:
        db.rollback()
        document.status = DocumentStatus.FAILED
        document.error = str(e)
        db.add(document)
        db.commit()
        raise