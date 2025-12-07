# Quickstart Guide: Docusaurus RAG Chatbot Integration

**Feature Branch**: `1-docusaurus-rag-chatbot` | **Date**: 2025-12-05 | **Plan**: [specs/1-docusaurus-rag-chatbot/plan.md](specs/1-docusaurus-rag-chatbot/plan.md)

This guide provides quick instructions to set up and run the Docusaurus RAG Chatbot locally.

## 1. Prerequisites

Before you begin, ensure you have the following installed:

-   **Python 3.9+**
-   **Node.js 18+** and **npm** or **yarn** (for Docusaurus)
-   **Docker Desktop** (optional, for containerized deployment)
-   Access to **Qdrant Cloud Free Tier** (or a local Qdrant instance)
-   **OpenAI API Key** (or ChatKit API Key, if applicable)

## 2. Backend Setup (FastAPI)

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

2.  **Create a virtual environment and install dependencies**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    pip install -r requirements.txt
    ```
    *(Note: `requirements.txt` will be created during implementation, containing `fastapi`, `uvicorn`, `qdrant-client`, `openai` / `langchain` / `llamaindex` etc.)*

3.  **Configure Environment Variables**:
    Create a `.env` file in the `backend/` directory with your API keys:
    ```ini
    QDRANT_API_KEY="your_qdrant_api_key"
    QDRANT_URL="your_qdrant_url" # e.g., https://[cluster-url]:6333
    OPENAI_API_KEY="your_openai_api_key"
    # CHATKIT_API_KEY="your_chatkit_api_key" # If using ChatKit
    ```

4.  **Run the FastAPI application**:
    ```bash
    uvicorn src.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.
    Refer to [specs/1-docusaurus-rag-chatbot/contracts/openapi.yaml](specs/1-docusaurus-rag-chatbot/contracts/openapi.yaml) for API endpoint details.

## 3. Frontend Setup (Docusaurus Widget)

1.  **Navigate to your Docusaurus project root**:
    ```bash
    cd frontend
    ```

2.  **Install dependencies**:
    ```bash
    npm install # or yarn install
    ```

3.  **Integrate the Chatbot Widget**:
    The lightweight JavaScript widget (e.g., a React component) will be provided and should be integrated into your Docusaurus site, likely by adding it to a Docusaurus layout component or via a plugin.
    *(Details on specific Docusaurus integration points will be provided during implementation.)*

4.  **Run Docusaurus**:
    ```bash
    npm start # or yarn start
    ```
    Your Docusaurus site with the chatbot will open in your browser.

## 4. Ingesting Content

Once the FastAPI backend is running, you can ingest your Docusaurus book content:

1.  **Send a POST request to the `/ingest` endpoint** (e.g., using `curl`, Postman, or a Python script):
    ```bash
    curl -X POST "http://localhost:8000/ingest" -H "Content-Type: application/json" -d '{}'
    ```
    This will process Markdown files from the Docusaurus `/docs` folder (relative to the backend service) and store embeddings in Qdrant.

## 5. Testing the Chatbot

1.  Open your Docusaurus site in the browser.
2.  Locate the chatbot bubble widget.
3.  Click the bubble to open the chat interface.
4.  Type a question related to your book content.
5.  (Optional) Highlight a section of text in your book, then ask a question to test "selected text only mode."

This will send queries to your FastAPI backend, which will use Qdrant for retrieval and an LLM for generation, displaying the answer in the chat widget.