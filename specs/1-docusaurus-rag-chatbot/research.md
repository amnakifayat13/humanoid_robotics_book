# Research Findings: RAG Chatbot Integration for Docusaurus

**Feature Branch**: `1-docusaurus-rag-chatbot` | **Date**: 2025-12-05 | **Plan**: [specs/1-docusaurus-rag-chatbot/plan.md](specs/1-docusaurus-rag-chatbot/plan.md)

This document consolidates research conducted to resolve technical unknowns and inform design decisions for the RAG Chatbot Integration feature.

## 1. Best Practices for Markdown Chunking in RAG

-   **Decision**: Utilize a multi-strategy approach for Markdown chunking:
    -   Prioritize Markdown's hierarchical structure (headers, code blocks) for initial splitting.
    -   Employ recursive character splitting with a hierarchy of separators (e.g., `\n\n` for paragraphs, then `\n` for lines, then sentence/word level if needed) to maintain contextual coherence within chunks.
    -   Experiment with various chunk sizes and overlapping chunks (e.g., 1-2 sentences of overlap) to optimize retrieval precision and context preservation.
    -   Consider token limits of the chosen embedding model and further split large chunks if necessary, ensuring that sentences and code blocks are preserved where possible.
    -   Enrich each chunk with hierarchical metadata (e.g., parent headers, document title) to provide context during retrieval and generation.
-   **Rationale**: This approach balances the need for smaller, retrievable units with the importance of preserving the natural contextual flow and structure of Markdown documents. Leveraging Markdown's native structure is efficient, and recursive splitting helps create semantically meaningful chunks. Overlapping and token-aware splitting mitigate the risk of losing context at chunk boundaries. Adding metadata enhances retrieval relevance.
-   **Alternatives Considered**:
    -   **Fixed-size character splitting**: Rejected due to its tendency to break sentences and code blocks, leading to poor contextual preservation and reduced retrieval accuracy.
    -   **Purely semantic chunking (embedding-based)**: While powerful, it adds complexity to the ingestion pipeline and may not always align with the explicit structural boundaries preferred in technical documentation like Docusaurus books. It can be explored as an optimization in future iterations if basic structural chunking proves insufficient.

## 2. Comparison of OpenAI vs. ChatKit Embedding Models

-   **Decision**: Initiate development using OpenAI embedding models, specifically `text-embedding-3-small` or `text-embedding-3-large`, as the primary choice.
-   **Rationale**: OpenAI embedding models are well-established, offer high semantic accuracy, contextual understanding, and have demonstrated strong performance in various RAG benchmarks. They are readily available via API, simplifying integration. A direct comparison with "ChatKit embedding models" was not found in public documentation, making OpenAI the more pragmatic and reliable choice for the initial implementation. The smaller `text-embedding-3-small` provides a cost-effective option, while `text-embedding-3-large` offers higher accuracy for more demanding scenarios.
-   **Alternatives Considered**:
    -   **Open-source embedding models (e.g., BGE-M3, Nomic-Embed)**: While offering cost advantages and self-hosting capabilities, they introduce additional complexity for deployment, management, and continuous updates compared to API-based solutions for this project's current scope. They are a viable option for future exploration if cost or data privacy becomes a more critical factor.
    -   **ChatKit embedding models**: Insufficient public information or direct comparison data to make an informed decision for initial implementation. Further research or clarification from the user would be required if ChatKit is a strict requirement.

## 3. Secure Handling of API Keys in Frontend and Backend

-   **Decision**:
    -   **Backend (FastAPI)**: All sensitive API keys (Qdrant, LLM, embedding service) will be stored as environment variables on the server. For production deployments, these will be managed through a dedicated Key Management Service (KMS) or a cloud-provider's secrets management solution (e.g., AWS Secrets Manager, Google Secret Manager, Azure Key Vault).
    -   **Frontend (Docusaurus Widget)**: No sensitive API keys will be directly exposed, stored, or accessed in the client-side Docusaurus JavaScript widget. All API calls requiring authentication with sensitive keys will be proxied through the FastAPI backend, adhering to a Backend-for-Frontend (BFF) pattern.
-   **Rationale**: This strategy rigorously follows the security principle of never exposing sensitive credentials in client-side code. Using environment variables is a standard practice for development and staging, while KMS provides robust, auditable, and encrypted storage for production secrets. The BFF pattern effectively isolates sensitive backend operations from potential frontend vulnerabilities, preventing unauthorized access and misuse of API keys.
-   **Alternatives Considered**:
    -   **Embedding keys directly in frontend with domain restrictions**: Rejected as inherently less secure and violates the principle of least privilege, even with strict restrictions. Potential for key leakage through browser extensions, developer tools, or cross-site scripting (XSS) attacks remains high.
    -   **Hardcoding keys in backend code**: Strictly forbidden due to severe security risks, poor operational practice, and risk of accidental exposure in version control.

## 4. FastAPI Deployment Options

-   **Decision**: Utilize Docker for local development and staging environments to ensure consistent setups and dependency management. For production, deploy the FastAPI backend using a Container-as-a-Service (CaaS) or Platform-as-a-Service (PaaS) solution (e.g., AWS App Runner, Render, AWS Elastic Beanstalk, Google Cloud Run, Azure Container Apps).
-   **Rationale**: Docker provides a lightweight, portable, and reproducible environment, simplifying development and ensuring consistency between different environments. CaaS/PaaS offerings abstract away much of the infrastructure management, providing features like automatic scaling, load balancing, health monitoring, and often simplified CI/CD integration. This reduces operational overhead and allows the team to focus on application development rather than infrastructure.
-   **Alternatives Considered**:
    -   **Self-managed Infrastructure-as-a-Service (IaaS) / Virtual Private Server (VPS)**: Rejected for the initial phase due to the higher operational burden of managing servers, operating systems, and networking, which is beyond the scope of a rapid feature integration.
    -   **Serverless functions (e.g., AWS Lambda, Google Cloud Functions)**: While viable for stateless APIs, a long-running FastAPI application with an ingestion endpoint that might involve significant processing (even if batched) could benefit from the more consistent resource allocation and startup times offered by containerized services. Serverless could be considered for specific, highly granular functions in a future iteration.