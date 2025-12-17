from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict
import logging
import os
from dotenv import load_dotenv

from agents.run import Runner, RunConfig
from agents import AsyncOpenAI, OpenAIChatCompletionsModel

# Import request/response models
from .models import (
    ChatRequest,
    SelectedTextChatRequest,
    ChatResponse,
    HealthResponse,
)

# Import MAIN agent
from agents_folder.rag_agent import main_agent

# Import Qdrant service
from services.qdrant_service import QdrantService
from services.embedding_service import EmbeddingService  # assuming a service to create embeddings

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in .env")

# Initialize FastAPI
app = FastAPI(
    title="OpenAI Agents RAG Chatbot API",
    description="RAG chatbot using OpenAI Agents SDK + Qdrant",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======================== Model & Runner Config =======================
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
)

# ======================== Services =======================
qdrant_service = QdrantService()
embedding_service = EmbeddingService()

async def fetch_qdrant_context(query: str, limit: int = 5) -> str:
    """Create embedding -> search Qdrant -> return combined context"""
    query_vector = await embedding_service.create_query_embedding(query)
    results = await qdrant_service.search_documentation(query_vector, limit)
    if not results:
        return "No relevant content found."
    context_strings = []
    for r in results:
        context_strings.append(f"{r.get('text','')} (Source: {r.get('metadata', {}).get('source_file','Unknown')})")
    return "\n\n".join(context_strings)

# =========================
# ROOT & HEALTH CHECK
# =========================
@app.get("/")
async def root() -> Dict[str, str]:
    return {
        "message": "OpenAI Agents RAG Chatbot API",
        "version": "1.0.0",
        "documentation": "/docs",
    }

@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        message="Service is operational",
    )

# =========================
# MAIN CHAT ENDPOINT
# =========================
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_documentation(chat_request: ChatRequest) -> ChatResponse:
    try:
        # 1️⃣ Fetch Qdrant context
        context_text = await fetch_qdrant_context(chat_request.message)

        # 2️⃣ Combine user input + context for the agent
        llm_input = f"Context:\n{context_text}\n\nQuestion:\n{chat_request.message}"

        # 3️⃣ Run the agent via Runner
        result = await Runner.run(
            main_agent,
            input=llm_input,
            run_config=config,
            context={"thread_id": chat_request.thread_id},
        )

        # Safely access sources from result, with fallback if metadata doesn't exist
        sources = []
        if hasattr(result, 'metadata') and result.metadata:
            sources = result.metadata.get("sources", [])
        elif hasattr(result, 'final_output') and result.final_output:
            # If there's no metadata, we can potentially extract sources from the output
            # For now, return empty list as fallback
            sources = []

        return ChatResponse(
            answer=result.final_output,
            thread_id=chat_request.thread_id,
            sources=sources,
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =========================
# SELECTED TEXT CHAT
# =========================
@app.post("/api/v1/chat/selected-text", response_model=ChatResponse)
async def chat_selected_text(chat_request: SelectedTextChatRequest) -> ChatResponse:
    try:
        # If user selected text, append it to context
        context_text = await fetch_qdrant_context(chat_request.selected_text)

        llm_input = f"Context:\n{context_text}\n\nQuestion:\n{chat_request.message}"

        result = await Runner.run(
            main_agent,
            input=llm_input,
            run_config=config,
            context={
                "thread_id": chat_request.thread_id,
                "selected_text": chat_request.selected_text,
            },
        )

        # Safely access sources from result, with fallback if metadata doesn't exist
        sources = []
        if hasattr(result, 'metadata') and result.metadata:
            sources = result.metadata.get("sources", [])
        elif hasattr(result, 'final_output') and result.final_output:
            # If there's no metadata, we can potentially extract sources from the output
            # For now, return empty list as fallback
            sources = []

        return ChatResponse(
            answer=result.final_output,
            thread_id=chat_request.thread_id,
            sources=sources,
        )

    except Exception as e:
        logger.error(f"Selected text chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =========================
# EXCEPTION HANDLERS
# =========================
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    logger.warning(f"404 error: {request.url}")
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "path": str(request.url)},
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error(f"500 error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )

# =========================
# LOGGING MIDDLEWARE
# =========================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
