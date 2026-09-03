from app.db import Base 
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as sqlEnum, JSON
from sqlalchemy.orm import relationship
from enum import Enum as pyEnum
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    email = Column(String, unique = True, nullable = False)
    hashed_password = Column(String, nullable = False)

class DocumentStatus(str, pyEnum):
    UPLOADED = "UPLOADED"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key = True)
    tenant_id = Column(String, nullable=False)
    filename = Column(String)
    status = Column(sqlEnum(DocumentStatus), nullable = False)
    storage_key = Column(String, nullable = False)
    document_metadata = Column(JSON, nullable = False)
    error = Column(String, nullable = True)
    created_at = Column(DateTime, server_default = func.now(), nullable = False)
    updated_at = Column(DateTime, server_default = func.now(), onupdate=func.now(), nullable = False)

    document_chunks = relationship("DocumentChunk", back_populates="document")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key = True)
    document_id = Column(Integer, ForeignKey(Document.id), nullable = False)
    chunk_index = Column(Integer, nullable = False)
    content = Column(String)
    embedding = Column(Vector(3072), nullable=False)
    document_metadata = Column(JSON)
    created_at = Column(DateTime, server_default = func.now(), nullable = False)
    document = relationship("Document", back_populates="document_chunks")