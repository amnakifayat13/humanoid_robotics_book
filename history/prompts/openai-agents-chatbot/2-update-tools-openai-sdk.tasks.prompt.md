---
id: 2
title: Update tools to OpenAI Agents SDK format
stage: tasks
date: 2025-12-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: openai-agents-chatbot
branch: 1-openai-agents-chatbot
user: Amna
command: "Update tools.py to use OpenAI Agents SDK format with @function_tool"
labels: ["tools", "openai-agents", "function-tool", "qdrant"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - C:\Amna\book\humanoid_robotics_book\backend\agents\tools.py
tests:
---

## Prompt

Update the tools.py file to use the OpenAI Agents SDK format with @function_tool decorator for the search_qdrant function and other tools.

## Response snapshot

Updated tools.py to use the OpenAI Agents SDK format:
- Imported Agent and function_tool from agents module
- Converted all tools to use @function_tool decorator
- Changed return types from Dict[str, Any] to str to match agent expectations
- Implemented proper async/await patterns for async functions
- Maintained the same functionality while adapting to the new framework
- Removed the ToolRegistry class in favor of standalone decorated functions
- Fixed the search_qdrant function to properly follow the example pattern

## Outcome

- ✅ Impact: Tools now compatible with OpenAI Agents SDK format
- 🧪 Tests: None added (implementation follows existing patterns)
- 📁 Files: Completely rewrote tools.py to use OpenAI Agents SDK
- 🔁 Next prompts: Test integration with OpenAI agents
- 🧠 Reflection: Successfully converted from ToolRegistry pattern to function_tool decorators

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test integration with OpenAI agents