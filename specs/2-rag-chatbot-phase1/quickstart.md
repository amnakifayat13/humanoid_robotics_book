# Quickstart: RAG Chatbot Data Pipeline and Qdrant Setup

## Prerequisites

- Python 3.11+
- pip package manager
- Git
- Qdrant Cloud account with API key
- Google Gemini API key
- Access to book-site/docs directory with markdown content

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the backend directory with:
   ```env
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   GEMINI_API_KEY=your_gemini_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

## Configuration

The system is configured through `backend/config/settings.py`. Key settings include:
- `MAX_CHUNK_SIZE`: Maximum size of text chunks (default: 1000 tokens)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200 tokens)
- API endpoints and authentication

## Running the Data Pipeline

1. **Execute the ingestion script**:
   ```bash
   cd backend
   python ingest.py
   ```

2. **Monitor the process**:
   The script will:
   - Read all .md and .mdx files from book-site/docs
   - Convert markdown to clean plain text
   - Split documents into chunks with overlap
   - Generate embeddings using Google Gemini
   - Store chunks in Qdrant vector database

3. **Verify completion**:
   Check the output for total files processed, chunks created, and vectors uploaded.

## API Endpoints (for later phases)

Once the backend API is implemented, the following endpoints will be available:
- `POST /api/ingest` - Trigger document ingestion
- `GET /api/status` - Check ingestion status
- `POST /api/search` - Perform semantic search against vector database

## Troubleshooting

- **API Rate Limits**: If you encounter rate limits with Gemini, adjust the batch size in the embedding service
- **Memory Issues**: For large documents, adjust chunk size settings in config
- **Qdrant Connection**: Verify URL and API key in environment variables
- **File Access**: Ensure the script has read access to the book-site/docs directory

## Next Steps

After successful data pipeline setup:
1. Implement the RAG chatbot API endpoints
2. Create the frontend chat interface
3. Integrate with the Docusaurus documentation site