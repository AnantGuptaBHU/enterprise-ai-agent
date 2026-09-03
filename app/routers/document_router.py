from fastapi import APIRouter, UploadFile, File
from app.storage.local import LocalStorage
from uuid import uuid4
router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)

storage = LocalStorage()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    document_id = uuid4()
    storage_key = f"documents/{document_id}/{file.filename}"

    stored_path = storage.save(file, storage_key)

    return {
        "document_id": str(document_id),
        "filename": file.filename,
        "content_type": file.content_type,
        "storage_key": storage_key,
        }