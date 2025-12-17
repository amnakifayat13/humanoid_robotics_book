---
id: 3
title: Update rag agent to OpenAI Agents SDK
stage: tasks
date: 2025-12-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: openai-agents-chatbot
branch: 1-openai-agents-chatbot
user: Amna
command: "Update rag_agent.py to use OpenAI Agents SDK with assistants API"
labels: ["agents", "openai-agents", "assistants-api", "rag", "qdrant"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - C:\Amna\book\humanoid_robotics_book\backend\agents\rag_agent.py
tests:
---

## Prompt

Update the rag-agent.py file to work with the OpenAI Agents SDK, using the assistants API with the function tools.

## Response snapshot

Updated rag_agent.py to use the OpenAI Assistants API:
- Created specialized assistants for RAG, greetings, and selected text queries
- Integrated the function tools (search_documentation, search_qdrant, greet_user) as assistant tools
- Implemented proper thread management for conversation persistence
- Maintained the same routing logic in MainRouterAgent
- Updated all methods to work with the assistants API instead of direct chat completions
- Added proper cleanup methods for assistants

## Outcome

- ✅ Impact: Agents now use OpenAI Assistants API with function tools
- 🧪 Tests: None added (implementation follows existing patterns)
- 📁 Files: Completely rewrote rag_agent.py to use OpenAI Assistants SDK
- 🔁 Next prompts: Test integration with OpenAI assistants API
- 🧠 Reflection: Successfully converted from direct API calls to assistants API with tool functions

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test integration with OpenAI assistants API