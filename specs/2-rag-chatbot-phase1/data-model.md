# Data Model: RAG Chatbot Data Pipeline and Qdrant Setup

## Document Chunk
Represents a segment of content from the original markdown files, including the text content, embedding vector, and metadata.

**Fields**:
- `id`: Unique identifier for the chunk (UUID string)
- `text`: The actual text content of the chunk (string)
- `embedding`: Vector representation of the text (array of floats, 768 dimensions for Gemini embeddings)
- `metadata`: Object containing document metadata
  - `source_file`: Original filename (string)
  - `relative_path`: Path relative to docs directory (string)
  - `full_path`: Complete file path (string)
- `size`: Character count of the text content (integer)

**Validation Rules**:
- `text` must not be empty
- `embedding` must be exactly 768 elements (for Gemini text-embedding-3-small)
- `size` must be positive
- `metadata` must contain required fields

## Document Metadata
Contains information about the source document including file path, relative path, filename, and full path.

**Fields**:
- `source_file`: Original filename from which the chunk was created (string)
- `relative_path`: Path relative to the book-site/docs directory (string)
- `full_path`: Complete absolute path to the source file (string)

**Validation Rules**:
- All fields must be non-empty strings
- `relative_path` must be a valid relative path
- `full_path` must be a valid absolute path

## Qdrant Collection Schema
Vector database storage unit that holds the document chunks with their embeddings for semantic search.

**Structure**:
- Collection name: "documentation_book"
- Vector size: 768 dimensions (matching Gemini embeddings)
- Distance metric: Cosine similarity
- Payload schema: Dynamic (Qdrant handles this automatically)

**Fields in Payload**:
- `text`: The chunk text content
- `metadata`: Object containing source document information
- `size`: The size of the chunk

## Processing State
Tracks the state of documents during the ingestion pipeline.

**Fields**:
- `file_path`: Path to the source file (string)
- `status`: Processing status (enum: "pending", "processing", "completed", "failed")
- `processed_chunks`: Number of chunks successfully processed (integer)
- `total_chunks`: Total number of chunks to process (integer)
- `error_message`: Error details if processing failed (string, optional)
- `timestamp`: When the processing started (ISO 8601 string)

**Validation Rules**:
- `status` must be one of the allowed values
- `processed_chunks` must be <= `total_chunks`
- `timestamp` must be a valid ISO 8601 string