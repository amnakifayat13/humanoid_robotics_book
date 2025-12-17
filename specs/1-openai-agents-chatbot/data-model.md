# Data Model: OpenAI Agents RAG Chatbot Implementation

## Entity: Chat Request
**Description**: Represents a user's request to the chatbot system
**Fields**:
- message: string (required) - The user's question or input text
- thread_id: string (optional) - Identifier for conversation context persistence

**Validation Rules**:
- message must not be empty or whitespace only
- message length should be within reasonable limits (e.g., 1-10000 characters)
- thread_id if provided must follow valid identifier format

## Entity: Selected Text Chat Request
**Description**: Represents a user's request with additional selected text context
**Fields**:
- message: string (required) - The user's question about the selected text
- selected_text: string (required) - The text content selected by the user
- thread_id: string (optional) - Identifier for conversation context persistence

**Validation Rules**:
- message must not be empty or whitespace only
- selected_text must not be empty or whitespace only
- message and selected_text should be within reasonable length limits
- thread_id if provided must follow valid identifier format

## Entity: Chat Response
**Description**: Represents the system's response to a user's chat request
**Fields**:
- answer: string (required) - The agent's response to the user's question
- thread_id: string (optional) - Identifier for conversation context persistence
- sources: array of objects (optional) - List of source citations if applicable

**Validation Rules**:
- answer must not be empty
- sources if provided must be an array of source objects with required properties
- thread_id if provided must follow valid identifier format

## Entity: Health Response
**Description**: Represents the system's health status
**Fields**:
- status: string (required) - Health status indicator (e.g., "healthy", "degraded", "unhealthy")
- message: string (required) - Descriptive message about the health status

**Validation Rules**:
- status must be one of predefined values: "healthy", "degraded", "unhealthy"
- message must not be empty

## Entity: Documentation Chunk
**Description**: Represents a chunk of documentation retrieved from the vector database
**Fields**:
- text: string (required) - The content of the documentation chunk
- score: number (required) - Relevance score from vector similarity search
- metadata: object (required) - Additional information about the source
  - source_file: string (required) - Name of the source file
  - relative_path: string (optional) - Relative path to the source file
  - full_path: string (optional) - Full path to the source file
- size: number (optional) - Size of the chunk in characters or tokens

**Validation Rules**:
- text must not be empty
- score must be a non-negative number
- metadata must contain at least source_file
- size if provided must be a positive number

## Entity: Agent Configuration
**Description**: Configuration parameters for the OpenAI agents
**Fields**:
- name: string (required) - Display name of the agent
- instructions: string (required) - Behavioral instructions for the agent
- tools: array of strings (optional) - List of tools the agent can use
- handoffs: array of agent references (optional) - List of agents this agent can handoff to

**Validation Rules**:
- name must not be empty
- instructions must not be empty
- tools if provided must reference valid tool names
- handoffs if provided must reference valid agent names

## Entity: Embedding Vector
**Description**: Represents a numerical embedding vector for semantic search
**Fields**:
- vector: array of numbers (required) - The embedding vector values
- model: string (required) - The model used to generate the embedding

**Validation Rules**:
- vector must be an array of numbers with consistent dimensions
- model must be a valid embedding model identifier
- vector length must match the expected dimension for the specified model