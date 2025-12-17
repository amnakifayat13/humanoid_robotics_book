# Quickstart Guide: OpenAI Agents RAG Chatbot

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Access to OpenAI API (for agents)
- Access to Google Gemini API (for embeddings)
- Access to Qdrant Cloud or local instance (for vector database)

## Environment Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install fastapi uvicorn qdrant-client google-generativeai openai pydantic
```

3. Create a `.env` file with the following environment variables:
```env
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
COLLECTION_NAME=documentation_chunks
DEBUG=True
HOST=0.0.0.0
PORT=8000
CHAT_MODEL=gpt-4-turbo-preview
```

## Running the Application

1. Start the FastAPI server:
```bash
cd backend
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

2. The API will be available at `http://localhost:8000`
3. API documentation will be available at `http://localhost:8000/docs`

## API Usage Examples

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### Chat with Documentation Agent
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the key components of a humanoid robot?"
  }'
```

### Chat with Selected Text Agent
```bash
curl -X POST http://localhost:8000/api/v1/chat/selected-text \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What does this text say about sensors?",
    "selected_text": "Humanoid robots use various sensors including cameras, accelerometers, and gyroscopes to perceive their environment."
  }'
```

## Architecture Overview

The system consists of:

1. **Services Layer**: Qdrant and embedding services for data operations
2. **Agents Layer**: Four specialized OpenAI agents with handoff patterns
3. **API Layer**: FastAPI application with health check and chat endpoints
4. **Tools Layer**: Custom function tools for vector search and greetings

## Key Endpoints

- `GET /` - API information
- `GET /api/v1/health` - Health check
- `POST /api/v1/chat` - Documentation RAG chat
- `POST /api/v1/chat/selected-text` - Selected text chat
- `GET /docs` - Interactive API documentation