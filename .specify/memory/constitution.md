<!-- Sync Impact Report:
Version change: 1.0.0 -> 1.0.1 (MINOR: Added project workflow integration section)
List of modified principles: N/A
Added sections:
  - Project Workflow Integration
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
  - .specify/templates/commands/sp.analyze.md: ⚠ pending
  - .specify/templates/commands/sp.adr.md: ⚠ pending
  - .specify/templates/commands/sp.implement.md: ⚠ pending
  - .specify/templates/commands/sp.git.commit_pr.md: ⚠ pending
  - .specify/templates/commands/sp.constitution.md: ⚠ pending
  - .specify/templates/commands/sp.clarify.md: ⚠ pending
  - .specify/templates/commands/sp.checklist.md: ⚠ pending
  - .specify/templates/commands/sp.plan.md: ⚠ pending
  - .specify/templates/commands/sp.phr.md: ⚠ pending
  - .specify/templates/commands/sp.specify.md: ⚠ pending
  - .specify/templates/commands/sp.tasks.md: ⚠ pending
Follow-up TODOs: Update templates to reflect new Project Workflow Integration section
-->
# Humanoid Robotics & Physical AI Constitution

## Core Principles

### I. Accuracy
No hallucinations. Verify robotics/AI facts.

### II. Coherence
All chapters must align with the master outline. Maintain consistent writing style, and structured progression from basics to advanced topics.

### III. Modularity
Allow chapters to be individually improved.

### IV. Transparency
Explain methodologies when needed.

### V. Safety
Address ethical implications of humanoids & embodied AI.

### VI. Creativity with Discipline

## Book Goals
- Explain humanoid robotics fundamentals, design, mechanics & kinematics.
- Cover physical AI, sensors, actuators, control systems.
- Explain reinforcement learning, imitation learning, embodied cognition.
- Include real-world case studies (Tesla Optimus, Boston Dynamics Atlas, etc.).
- Provide code samples for simulation & robotics control.
- Include diagrams, architecture blueprints, and tables.
- Explain safety, ethics, governance, and future of physical AI.

## Writing Style Rules
- Clear, concise, engaging — like a high-level technical textbook + friendly guide.
- Use simple explanations first → then advanced breakdowns.
- Each chapter ends with:
  - Summary
  - Key terms
  - Practical exercises

## AI Collaboration Rules
- **Claude** handles: deep reasoning, chapter planning, theoretical explanations, structure, editing.
- **Gemini** handles: factual accuracy, robotics physics, formulas, diagrams, examples.
- SpecKit blends all outputs into consistent, high-quality content.

## Project Workflow Integration
- RAG Chatbot Engineering: Integrated RAG Chatbot using FastAPI backend, Qdrant Cloud Free Tier (vector DB), ChatKit (OpenAI Agents SDK), and Google Gemini text-embedding-3-small as the embedding model.
- Data Pipeline: Markdown reader for book-site/docs, text conversion to clean plain text, chunking strategy with overlap, embedding generation, and Qdrant vector database integration.
- @project_workflow: See rag-chatbot-spec.md for complete implementation details including backend structure, API endpoints, and deployment configuration.

## Governance
Constitution supersedes all other practices; Amendments require documentation, approval, migration plan.

**Operational Mode:**
- When the user gives **/sp.plan**, generate the book plan.
- When user gives **/sp.spec**, generate detailed chapter specifications.
- When user gives **/sp.implement**, begin writing chapters.
- When user requests revisions, implement changes without losing style consistency.

**Version**: 1.0.1 | **Ratified**: 2025-12-03 | **Last Amended**: 2025-12-15