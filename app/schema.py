from pydantic import BaseModel, Field
from typing import Any


class IngestionRequest(BaseModel):
    tenant_id: str
    storage_key: str
    filename: str
    metadata: dict[str, Any] = Field(default_factory=dict)