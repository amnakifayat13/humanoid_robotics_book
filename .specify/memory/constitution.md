<!-- Sync Impact Report:
Version change: 0.0.0 -> 1.0.0 (MAJOR: Initial version from new user input)
List of modified principles:
  - Added: Accuracy
  - Added: Coherence
  - Added: Modularity
  - Added: Transparency
  - Added: Safety
  - Added: Creativity with Discipline
Added sections:
  - Book Goals
  - Writing Style Rules
  - AI Collaboration Rules
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ updated
  - .specify/templates/spec-template.md: ✅ updated
  - .specify/templates/tasks-template.md: ✅ updated
  - .specify/templates/commands/sp.analyze.md: ✅ updated
  - .specify/templates/commands/sp.adr.md: ✅ updated
  - .specify/templates/commands/sp.implement.md: ✅ updated
  - .specify/templates/commands/sp.git.commit_pr.md: ✅ updated
  - .specify/templates/commands/sp.constitution.md: ✅ updated
  - .specify/templates/commands/sp.clarify.md: ✅ updated
  - .specify/templates/commands/sp.checklist.md: ✅ updated
  - .specify/templates/commands/sp.plan.md: ✅ updated
  - .specify/templates/commands/sp.phr.md: ✅ updated
  - .specify/templates/commands/sp.specify.md: ✅ updated
  - .specify/templates/commands/sp.tasks.md: ✅ updated
Follow-up TODOs: N/A
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

## Governance
Constitution supersedes all other practices; Amendments require documentation, approval, migration plan.

**Operational Mode:**
- When the user gives **/sp.plan**, generate the book plan.
- When user gives **/sp.spec**, generate detailed chapter specifications.
- When user gives **/sp.implement**, begin writing chapters.
- When user requests revisions, implement changes without losing style consistency.

**Version**: 1.0.0 | **Ratified**: 2025-12-03 | **Last Amended**: 2025-12-03
