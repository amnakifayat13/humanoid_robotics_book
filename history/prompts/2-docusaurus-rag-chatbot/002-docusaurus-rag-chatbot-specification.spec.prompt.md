---
id: 002
title: Docusaurus RAG Chatbot Specification
stage: spec
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 2-docusaurus-rag-chatbot
branch: 2-docusaurus-rag-chatbot
user: user
command: /sp.specify
labels: ["rag","docusaurus","chatbot","specification"]
links:
  spec: specs/2-docusaurus-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/2-docusaurus-rag-chatbot/spec.md
  - specs/2-docusaurus-rag-chatbot/checklists/requirements.md
tests:
  - None
---

## Prompt

You are an AI architect. Create a complete SpecKit specification for integrating a Retrieval-Augmented Generation (RAG) chatbot inside a Docusaurus book.

Key Requirements:
1. Extract all book content from the Docusaurus /docs folder.
2. Convert Markdown (.md) files into clean text, preserving headings and subheadings.
3. Generate vector embeddings using OpenAI Agents SDK or ChatKit embedding models.
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

Return the final specification in a clean, multi-section SpecKit format.

## Response snapshot

The specification for "Docusaurus RAG Chatbot Integration" has been successfully created and validated. All checklist items are complete, and the feature is ready for the planning phase. You can now proceed to planning using `/sp.plan`.

## Outcome

- ✅ Impact: Feature specification for Docusaurus RAG Chatbot created.
- 🧪 Tests: None (specification generated)
- 📁 Files: specs/2-docusaurus-rag-chatbot/spec.md, specs/2-docusaurus-rag-chatbot/checklists/requirements.md
- 🔁 Next prompts: User should run `/sp.plan`
- 🧠 Reflection: The initial branch name was too long, requiring manual branch creation. The specification itself was generated and validated successfully without needing clarifications.

## Evaluation notes (flywheel)

- Failure modes observed: Bash script for PHR creation failed due to path length limit. Manual PHR creation was performed.
- Graders run and results (PASS/FAIL): None
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Ensure robustness of create-new-feature.ps1 for long feature descriptions.
