# Feature Specification: RAG Chatbot Integration for Docusaurus

**Feature Branch**: `1-docusaurus-rag-chatbot`
**Created**: 2025-12-05
**Status**: Draft
**Input**: User description: "You are an AI architect. Create a complete SpecKit specification for integrating a Retrieval-Augmented Generation (RAG) chatbot inside a Docusaurus book.

Key Requirements:
1. Extract all book content from the Docusaurus /docs folder.
2. Convert Markdown (.md) files into clean text, preserving headings and subheadings.
3. Generate vector embeddings using OpenAI or ChatKit embedding models.
4. Store embeddings inside Qdrant Cloud Free Tier (using collection = "book_rag").
5. Build a FastAPI backend with the following endpoints:
   - POST /ingest → ingest all book chapters into Qdrant
   - POST /search → perform semantic search using Qdrant
   - POST /ask → combine search results + user query → call LLM to generate the answer
6. The chatbot must answer questions based ONLY on the retrieved book content.
7. Add support for “selected text only mode”: if the user highlights text inside the book, the chatbot must restrict answers to that specific text.
8. Create a lightweight JavaScript widget (chat bubble) that embeds the chatbot inside the Docusaurus site.
9. Ensure secure handling of Qdrant API keys and LLM API keys.
10. Describe the whole pipeline: ingestion, indexing, retrieval, generation, and frontend integration.

Return the final specification in a clean, multi-section SpecKit format."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask Questions on Book Content (Priority: P1)

As a Docusaurus book reader, I want to ask questions about the book content through a chatbot and receive accurate answers based *only* on the book's content, so I can quickly understand concepts and find information.

**Why this priority**: This is the core functionality and provides immediate value to the reader.

**Independent Test**: A user can open the Docusaurus site, interact with the chat bubble, ask a question, and receive a relevant answer sourced solely from the book.

**Acceptance Scenarios**:

1.  **Given** the Docusaurus site is open and the chatbot widget is visible, **When** a user clicks the chat bubble and types a question, **Then** the chatbot displays a concise answer derived from the book's content.
2.  **Given** the chatbot is active, **When** a user asks a question whose answer is not present in the book, **Then** the chatbot indicates it cannot find relevant information in the book.

---

### User Story 2 - Contextual Answers with Selected Text (Priority: P2)

As a Docusaurus book reader, I want the chatbot to restrict its answers to a specific highlighted text selection within the book, so I can get highly focused information relevant to what I'm currently reading.

**Why this priority**: Enhances the precision of the chatbot and provides a powerful contextual interaction.

**Independent Test**: A user can highlight a paragraph in the Docusaurus book, activate the chatbot in "selected text only mode", ask a question, and receive an answer limited to the highlighted text.

**Acceptance Scenarios**:

1.  **Given** a user has highlighted text in the Docusaurus book and activates "selected text only mode", **When** the user asks a question, **Then** the chatbot provides an answer based *only* on the highlighted text.
2.  **Given** "selected text only mode" is active, **When** the user asks a question whose answer is not in the highlighted text but *is* in the broader book content, **Then** the chatbot indicates it cannot find relevant information within the selected text.

---

### User Story 3 - Ingest Book Content (Priority: P3)

As a book administrator, I want to trigger an ingestion process to extract, process, embed, and store all Docusaurus `/docs` content into Qdrant, so the chatbot has an up-to-date knowledge base.

**Why this priority**: Essential for keeping the chatbot's knowledge base current, but not a direct reader interaction.

**Independent Test**: An administrator can initiate the ingestion process, verify that Markdown files from `/docs` are processed into clean text, vector embeddings are generated, and these embeddings are successfully stored in the "book_rag" collection in Qdrant.

**Acceptance Scenarios**:

1.  **Given** a Docusaurus book with content in `/docs`, **When** the `/ingest` endpoint is called, **Then** all Markdown files are extracted, converted to clean text preserving headings, and their embeddings are stored in Qdrant's "book_rag" collection.
2.  **Given** the ingestion process completes, **When** new content is added to `/docs`, **Then** subsequent ingestion correctly updates or adds the new content to Qdrant.

---

### Edge Cases

- What happens when the Docusaurus `/docs` folder is empty or contains no Markdown files?
- How does the system handle very large Markdown files during ingestion (e.g., memory limits, chunking strategy)?
- What happens if the Qdrant Cloud Free Tier limits are exceeded (e.g., storage, request rate)?
- How does the system handle network failures or API key authentication issues with OpenAI/ChatKit or Qdrant during embedding generation or storage?
- What happens if the LLM call fails or returns an inappropriate response?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST extract all Markdown (`.md`) files from the Docusaurus `/docs` folder.
- **FR-002**: The system MUST convert extracted Markdown content into clean text, preserving headings and subheadings.
- **FR-003**: The system MUST generate vector embeddings for the cleaned text using either OpenAI or ChatKit embedding models.
- **FR-004**: The system MUST store the generated vector embeddings in Qdrant Cloud Free Tier, specifically in a collection named "book_rag".
- **FR-005**: The system MUST provide a FastAPI backend.
- **FR-006**: The FastAPI backend MUST expose a `POST /ingest` endpoint to trigger the content extraction, conversion, embedding, and storage process into Qdrant.
- **FR-007**: The FastAPI backend MUST expose a `POST /search` endpoint to perform semantic search queries against the Qdrant index.
- **FR-008**: The FastAPI backend MUST expose a `POST /ask` endpoint that takes a user query, combines it with search results from Qdrant, and calls an LLM to generate an answer.
- **FR-009**: The chatbot MUST generate answers based ONLY on the retrieved book content.
- **FR-010**: The chatbot MUST support a "selected text only mode" where answers are restricted to a user-highlighted text segment from the book.
- **FR-011**: The system MUST include a lightweight JavaScript widget (chat bubble) that embeds the chatbot functionality into the Docusaurus site.
- **FR-012**: The system MUST securely handle Qdrant API keys and LLM API keys.
- **FR-013**: The system MUST describe the entire RAG pipeline: ingestion, indexing, retrieval, generation, and frontend integration.

### Key Entities *(include if feature involves data)*

-   **Book Content**: Raw Markdown files from `/docs`, cleaned text, and their corresponding vector embeddings.
-   **Qdrant Collection**: The "book_rag" collection in Qdrant storing vector embeddings and metadata.
-   **User Query**: The question or highlighted text provided by the Docusaurus reader.
-   **LLM Response**: The generated answer from the Large Language Model.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The `/ingest` endpoint successfully processes all Markdown files in `/docs` and updates Qdrant within 5 minutes.
- **SC-002**: 95% of user questions through the chatbot receive relevant answers within 5 seconds, based solely on the book content.
- **SC-003**: In "selected text only mode," 98% of answers are correctly constrained to the highlighted text.
- **SC-004**: Qdrant and LLM API keys are stored and accessed without exposing them in client-side code or insecure server logs.
- **SC-005**: The chatbot widget loads and is interactive on Docusaurus pages without significantly impacting page load times (e.g., adds less than 500ms to Largest Contentful Paint).