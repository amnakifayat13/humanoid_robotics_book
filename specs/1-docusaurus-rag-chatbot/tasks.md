# Tasks: RAG Chatbot Integration for Docusaurus

**Input**: Design documents from `/specs/1-docusaurus-rag-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: The feature specification did not explicitly request test tasks. However, unit and integration testing tasks are included in the "Polish & Cross-Cutting Concerns" phase to ensure quality.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`,`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create `backend/`  directories at repository root
- [x] T002 Initialize Python environment in `backend/` and create `backend/requirements.txt`
- [x] T003 [P] Add core backend dependencies (`fastapi`, `uvicorn`, `qdrant-client`, `chatkit`) to `backend/requirements.txt`
- [x] T004 [P] Initialize Node.js environment in `book-site/` and create `book-site/package.json` with basic `react` and `docusaurus` dependencies
- [ ] T005 [P] Create `.env.example` file in `backend/` for API key configuration documentation
- [ ] T006 [P] Create initial `backend/src/main.py` with basic FastAPI application setup
- [ ] T007 [P] Create placeholder files for backend structure (e.g., `backend/src/api/__init__.py`, `backend/src/services/__init__.py`, `backend/src/models/__init__.py`, `backend/src/config.py`)
- [ ] T008 [P] Create placeholder files for frontend structure (e.g., `book-site/src/components/ChatbotWidget.js`, `book-site/src/services/api.js`, `book-site/src/hooks/useChat.js`, `book-site/src/theme/Layout/index.js`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 Implement secure API key loading mechanism from environment variables in `backend/src/config.py`
- [ ] T010 [P] Create `QdrantClient` instance and basic connection logic in `backend/src/services/qdrant_service.py`
- [ ] T011 [P] Implement `MarkdownChunker` utility for text extraction and recursive splitting in `backend/src/services/data_processing.py`
- [ ] T012 [P] Implement `EmbeddingGenerator` utility using OpenAI API in `backend/src/services/embedding_service.py`
- [ ] T013 Create Qdrant collection `book_rag` with appropriate vector size and configuration (based on embedding model) in `backend/src/services/qdrant_service.py` (`create_collection` method)
- [ ] T014 Configure basic logging for FastAPI application in `backend/src/main.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Ask Questions on Book Content (Priority: P1) 🎯 MVP

**Goal**: As a Docusaurus book reader, I want to ask questions about the book content through a chatbot and receive accurate answers based *only* on the book's content, so I can quickly understand concepts and find information.

**Independent Test**: A user can open the Docusaurus site, interact with the chat bubble, ask a question, and receive a relevant answer sourced solely from the book.

### Implementation for User Story 1

- [ ] T015 [US1] Define `AskRequest` and `LLMResponse` Pydantic models in `backend/src/models/chatbot.py` based on `contracts/openapi.yaml`
- [ ] T016 [P] [US1] Implement semantic search logic using Qdrant client in `backend/src/services/qdrant_service.py` (`search_chunks` method)
- [ ] T017 [P] [US1] Implement LLM answer generation logic using retrieved context in `backend/src/services/llm_service.py` (`generate_answer` method)
- [ ] T018 [US1] Implement `POST /ask` endpoint in `backend/src/api/chatbot.py` to orchestrate Qdrant search and LLM services
- [ ] T019 [P] [US1] Create basic chat bubble component in `book-site/src/components/ChatBubble.js` with toggle functionality
- [ ] T020 [P] [US1] Create basic chat window component in `book-site/src/components/ChatWindow.js` to display messages
- [ ] T021 [P] [US1] Implement frontend API client for `POST /ask` endpoint in `book-site/src/services/api.js`
- [ ] T022 [US1] Integrate `ChatbotWidget` (containing bubble and window) into Docusaurus site layout (e.g., `book-site/src/theme/Layout/index.js`)
- [ ] T023 [US1] Implement state management for chat interaction (user input, messages, loading state) in `book-site/src/hooks/useChat.js`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Contextual Answers with Selected Text (Priority: P2)

**Goal**: As a Docusaurus book reader, I want the chatbot to restrict its answers to a specific highlighted text selection within the book, so I can get highly focused information relevant to what I'm currently reading.

**Independent Test**: A user can highlight a paragraph in the Docusaurus book, activate the chatbot in "selected text only mode", ask a question, and receive an answer limited to the highlighted text.

### Implementation for User Story 2

- [ ] T024 [P] [US2] Implement frontend hook `book-site/src/hooks/useTextSelection.js` to capture highlighted text and current page URL
- [ ] T025 [US2] Update `AskRequest` Pydantic model in `backend/src/models/chatbot.py` to include `selected_text` and `context_url`
- [ ] T026 [US2] Modify `POST /ask` endpoint logic in `backend/src/api/chatbot.py` to leverage `selected_text` and `context_url` for contextual retrieval/generation
- [ ] T027 [P] [US2] Enhance `EmbeddingGenerator` to handle smaller `selected_text` inputs for embedding (if needed for filtering) in `backend/src/services/embedding_service.py`
- [ ] T028 [US2] Update `book-site/src/components/ChatbotWidget.js` and `book-site/src/hooks/useChat.js` to enable "selected text only mode" UI and pass `selected_text` to API
- [ ] T029 [US2] Refine `backend/src/services/qdrant_service.py` search logic to prioritize or filter by `selected_text` and `context_url` metadata if provided in query
- [ ] T030 [US2] Refine `backend/src/services/llm_service.py` generation logic to strictly adhere to `selected_text` when present in context, potentially by modifying prompt.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Ingest Book Content (Priority: P3)

**Goal**: As a book administrator, I want to trigger an ingestion process to extract, process, embed, and store all Docusaurus `/docs` content into Qdrant, so the chatbot has an up-to-date knowledge base.

**Independent Test**: An administrator can initiate the ingestion process, verify that Markdown files from `/docs` are processed into clean text, vector embeddings are generated, and these embeddings are successfully stored in the "book_rag" collection in Qdrant.

### Implementation for User Story 3

- [ ] T031 [US3] Implement Docusaurus `/docs` content extraction and Markdown parsing in `backend/src/services/document_loader.py`
- [ ] T032 [US3] Implement full ingestion pipeline: load, clean, chunk, embed, store (`DocumentChunk` creation and Qdrant upsert) in `backend/src/services/ingestion_service.py`
- [ ] T033 [US3] Define `IngestRequest` Pydantic model in `backend/src/models/ingestion.py` based on `contracts/openapi.yaml`
- [ ] T034 [US3] Implement `POST /ingest` endpoint in `backend/src/api/ingestion.py` to trigger the ingestion service
- [ ] T035 [US3] Add optional `clear_existing` logic to `ingestion_service.py` to clear the Qdrant collection before new ingestion
- [ ] T036 [US3] Ensure ingestion gracefully handles empty `/docs` folder or no Markdown files in `backend/src/services/document_loader.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T037 Refine error handling across backend endpoints (e.g., specific HTTP status codes, detailed error messages) in `backend/src/api/` and `backend/src/services/`
- [ ] T038 Implement comprehensive backend unit tests for services and API endpoints in `backend/tests/unit/` (covering `qdrant_service`, `llm_service`, `embedding_service`, `data_processing`, `ingestion_service`, `api`)
- [ ] T039 Implement backend integration tests for the full RAG pipeline (ingest → search → ask) in `backend/tests/integration/`
- [ ] T040 Implement frontend unit tests for React components and hooks in `frontend/tests/unit/` (covering `ChatbotWidget`, `useChat`, `useTextSelection`)
- [ ] T041 [P] Update `backend/requirements.txt` with exact pinned versions of all dependencies
- [ ] T042 [P] Update `book-site/package.json` with exact pinned versions of all dependencies
- [ ] T043 [P] Document deployment steps for a chosen CaaS/PaaS (e.g., Dockerfile, cloud provider specific configuration files) in `docs/deployment/` or `backend/deployment/`
- [ ] T044 Review and update `specs/1-docusaurus-rag-chatbot/quickstart.md` for accuracy, completeness, and user-friendliness
- [ ] T045 Conduct security review of API key handling and data flow to ensure no vulnerabilities or sensitive data leakage
- [ ] T046 Optimize embedding generation and Qdrant search for performance within Free Tier limits, potentially including batching or indexing strategies.

---

## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately
-   **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
-   **User Stories (Phase 3, 4, 5)**: All depend on Foundational phase completion
    -   User stories can then proceed in parallel (if staffed)
    -   Or sequentially in priority order (P1 → P2 → P3)
-   **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

-   **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
-   **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1's `POST /ask` endpoint and backend models, but should be independently testable for its core functionality.
-   **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No direct dependencies on US1 or US2 for its core ingestion functionality.

### Within Each User Story

-   Models before services
-   Services before endpoints
-   Core implementation before integration
-   Story complete before moving to next priority

### Parallel Opportunities

-   All Setup tasks marked [P] can run in parallel (T003, T004, T005, T006, T007, T008)
-   All Foundational tasks marked [P] can run in parallel (T010, T011, T012)
-   Once Foundational phase completes, User Stories 1, 2, and 3 can technically begin in parallel (if team capacity allows, respecting US2's soft dependency on US1's API structure).
-   Tasks within a story marked [P] (e.g., T016, T017, T019, T020, T021 for US1) can run in parallel.
-   Different user stories can be worked on in parallel by different team members.

---

## Parallel Example: User Story 1 (Ask Questions on Book Content)

```bash
# Launch parallel tasks for User Story 1:
Task: "Define AskRequest and LLMResponse Pydantic models in backend/src/models/chatbot.py"
Task: "Implement semantic search logic using Qdrant client in backend/src/services/qdrant_service.py"
Task: "Implement LLM answer generation logic using retrieved context in backend/src/services/llm_service.py"
Task: "Create basic chat bubble component in frontend/src/components/ChatBubble.js"
Task: "Create basic chat window component in frontend/src/components/ChatWindow.js"
Task: "Implement frontend API client for POST /ask endpoint in frontend/src/services/api.js"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Test User Story 1 independently (user can ask questions and get answers from the book content).
5.  Deploy/demo if ready

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3.  Add User Story 2 → Test independently → Deploy/Demo
4.  Add User Story 3 → Test independently → Deploy/Demo
5.  Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    -   Developer A: User Story 1 (Ask Questions)
    -   Developer B: User Story 3 (Ingest Content) - can run largely in parallel with A.
    -   Developer C: User Story 2 (Selected Text Mode) - can start after US1's core API is defined.
3.  Stories complete and integrate independently.

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Verify tests fail before implementing (if test tasks are included and followed in a TDD manner)
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence