# Data Model: RAG Chatbot Integration for Docusaurus

**Feature Branch**: `1-docusaurus-rag-chatbot` | **Date**: 2025-12-05 | **Spec**: [specs/1-docusaurus-rag-chatbot/spec.md](specs/1-docusaurus-rag-chatbot/spec.md)

This document describes the key data entities and their relationships for the RAG Chatbot Integration feature.

## 1. DocumentChunk

Represents a small, semantically meaningful portion of the Docusaurus book content, suitable for embedding and retrieval.

-   **`id`**: Unique identifier for the chunk (e.g., UUID).
-   **`content`**: The cleaned text content of the chunk.
-   **`vector`**: The vector embedding generated from `content`.
-   **`metadata`**: Structured information about the chunk's origin and context.
    -   **`source_file`**: Original Markdown file path (e.g., `/docs/chapter1.md`).
    -   **`title`**: Title of the document or closest heading.
    -   **`section`**: Closest subheading.
    -   **`page_url`**: URL of the Docusaurus page where the content resides.
    -   **`start_line`**: Starting line number of the chunk in the original file.
    -   **`end_line`**: Ending line number of the chunk in the original file.
    -   **`highlight_text`**: (Optional) Boolean flag or unique identifier to link to specific highlighted text in frontend.

## 2. BookDocument

Represents a full Markdown file from the Docusaurus `/docs` directory before chunking.

-   **`path`**: Absolute path to the Markdown file.
-   **`raw_content`**: Original Markdown content.
-   **`cleaned_text`**: Content after Markdown-to-text conversion, preserving structure.
-   **`chunks`**: A list of `DocumentChunk` objects derived from this document.

## 3. UserQuery

Represents the input from the Docusaurus reader.

-   **`text`**: The question asked by the user.
-   **`selected_text`**: (Optional) The text highlighted by the user in "selected text only mode."
-   **`context_url`**: (Optional) The URL of the Docusaurus page from which the query was made.

## 4. LLMResponse

Represents the generated answer from the Large Language Model.

-   **`answer`**: The generated text response.
-   **`source_chunks`**: (Optional) A list of `DocumentChunk` IDs that were used to generate the answer.
-   **`confidence`**: (Optional) A score indicating the LLM's confidence in the answer.
-   **`error_message`**: (Optional) Message indicating if an answer could not be generated (e.g., no relevant content found).

## 5. APIKey

Represents a credential for interacting with external services.

-   **`name`**: Identifier for the API key (e.g., "QDRANT_API_KEY", "OPENAI_API_KEY").
-   **`value`**: The actual key string (securely stored).
-   **`service`**: The service this key is for (e.g., "Qdrant", "OpenAI", "ChatKit").
-   **`type`**: (e.g., "embedding", "llm", "vector_db").

## Relationships

-   `BookDocument` 1-to-many `DocumentChunk`: Each book document is broken down into multiple chunks.
-   `UserQuery` to `Qdrant Collection`: User queries are used to search the `Qdrant Collection` of `DocumentChunk` vectors.
-   `Qdrant Collection` to `LLMResponse`: Retrieved `DocumentChunk`s are provided as context to the LLM for generating an `LLMResponse`.
-   `APIKey` to various services: `APIKey`s are used to authenticate interactions with Qdrant, embedding models, and LLMs.