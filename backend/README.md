# RAG Chatbot Data Pipeline Backend

This backend service handles the data ingestion pipeline for the RAG chatbot system. It reads markdown files, processes them, generates embeddings, and stores them in a vector database for semantic search.

## Architecture

The system is organized into several modules:

- `data_ingestion/` - Core processing modules
  - `markdown_reader.py` - Reads markdown files from the documentation directory
  - `text_converter.py` - Converts markdown to clean plain text
  - `chunker.py` - Splits documents into overlapping chunks
  - `embedding_service.py` - Generates embeddings using Google Gemini
  - `qdrant_client.py` - Stores chunks in Qdrant vector database
  - `models.py` - Data models for the system
- `config/` - Configuration management
  - `settings.py` - Application settings and environment variables
- `utils/` - Utility functions
  - Contains logging and error handling infrastructure

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file in the backend directory with:
   ```env
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   GEMINI_API_KEY=your_gemini_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

3. **Configure settings** (optional):
   Adjust settings in `config/settings.py` or via environment variables:
   - `MAX_CHUNK_SIZE`: Maximum size of text chunks (default: 1000)
   - `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
   - `BATCH_SIZE`: Batch size for API calls (default: 10)

## Usage

### Run the ingestion pipeline:
```bash
python ingest.py
```

This will:
1. Read all markdown files from `../../book-site/docs` (configurable)
2. Convert markdown to clean plain text
3. Split documents into overlapping chunks
4. Generate embeddings using Google Gemini
5. Store chunks in Qdrant vector database

### Environment Variables

- `QDRANT_URL`: URL for your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant
- `GEMINI_API_KEY`: Google Gemini API key
- `MAX_CHUNK_SIZE`: Maximum chunk size in characters (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks in characters (default: 200)
- `BATCH_SIZE`: Batch size for embedding generation (default: 10)
- `DOCS_DIR`: Directory containing markdown files (default: `../../book-site/docs`)
- `COLLECTION_NAME`: Qdrant collection name (default: `documentation_book`)

## Data Flow

1. **Read**: Markdown files are read from the configured documentation directory
2. **Convert**: Markdown is converted to clean plain text while preserving important content
3. **Chunk**: Documents are split into overlapping chunks of configurable size
4. **Embed**: Each chunk gets a vector embedding using Google Gemini's text-embedding-3-small model
5. **Store**: Chunks with embeddings are stored in Qdrant vector database for semantic search

## Testing

Run the tests with pytest:
```bash
pytest tests/
```

## Error Handling

The system implements graceful error handling:
- Individual file processing failures don't stop the entire pipeline
- Detailed logging for debugging
- Validation at each processing step
- Fallback mechanisms for API failures