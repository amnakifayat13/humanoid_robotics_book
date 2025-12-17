from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from uuid import UUID
import uuid


class DocumentMetadata(BaseModel):
    """
    Model representing metadata for a source document.
    """
    source_file: str = Field(..., description="Original filename from which the chunk was created")
    relative_path: str = Field(..., description="Path relative to the book-site/docs directory")
    full_path: str = Field(..., description="Complete absolute path to the source file")

    @validator('source_file', 'relative_path', 'full_path')
    def validate_non_empty_string(cls, v):
        if not v or not v.strip():
            raise ValueError('Field must be a non-empty string')
        return v


class ProcessingState(BaseModel):
    """
    Model tracking the state of documents during the ingestion pipeline.
    """
    file_path: str = Field(..., description="Path to the source file")
    status: str = Field(..., description="Processing status", pattern=r"^(pending|processing|completed|failed)$")
    processed_chunks: int = Field(..., description="Number of chunks successfully processed", ge=0)
    total_chunks: int = Field(..., description="Total number of chunks to process", ge=0)
    error_message: Optional[str] = Field(None, description="Error details if processing failed")
    timestamp: str = Field(..., description="When the processing started (ISO 8601 string)")

    @validator('processed_chunks', 'total_chunks')
    def validate_counts(cls, v):
        if v < 0:
            raise ValueError('Count must be non-negative')
        return v

    @validator('processed_chunks')
    def validate_processed_chunks(cls, v, values):
        if 'total_chunks' in values and v > values['total_chunks']:
            raise ValueError('processed_chunks cannot exceed total_chunks')
        return v


class DocumentChunk(BaseModel):
    """
    Model representing a segment of content from the original markdown files.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the chunk")
    text: str = Field(..., description="The actual text content of the chunk", min_length=1)
    embedding: List[float] = Field(..., description="Vector representation of the text", min_items=768, max_items=768)
    metadata: DocumentMetadata = Field(..., description="Object containing document metadata")
    size: int = Field(..., description="Character count of the text content", gt=0)

    @validator('embedding')
    def validate_embedding_length(cls, v):
        if len(v) != 768:
            raise ValueError(f'Embedding must have exactly 768 elements, got {len(v)}')
        if not all(isinstance(x, (int, float)) for x in v):
            raise ValueError('All embedding values must be numeric')
        return v

    @validator('size')
    def validate_size(cls, v):
        if v <= 0:
            raise ValueError('Size must be positive')
        return v

    @validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Text must not be empty')
        return v.strip()


class IngestionResult(BaseModel):
    """
    Model representing the result of an ingestion operation.
    """
    success: bool = Field(..., description="Whether the ingestion was successful")
    processed_files: int = Field(..., description="Number of files processed")
    total_chunks: int = Field(..., description="Total number of chunks created")
    errors: List[str] = Field(default=[], description="List of errors that occurred during ingestion")
    processing_time: float = Field(..., description="Time taken to process in seconds")