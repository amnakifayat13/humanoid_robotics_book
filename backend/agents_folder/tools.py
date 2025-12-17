from agents import Agent, function_tool
from typing import Dict, Any
from services.qdrant_service import QdrantService
from services.embedding_service import EmbeddingService

# Initialize services globally
qdrant_service = QdrantService()
embedding_service = EmbeddingService()


@function_tool
async def search_documentation(query: str) -> str:
    """Search documentation based on the query and return relevant chunks"""
    try:
        # Create embedding for the query
        query_vector = await embedding_service.create_query_embedding(query)

        # Search documentation using Qdrant
        results = await qdrant_service.search_documentation(query_vector, limit=5)

        # Convert results to string format for the agent
        result_strings = []
        for result in results:
            if isinstance(result, dict):
                result_strings.append(f"Content: {result.get('content', '')}\nSource: {result.get('source', 'Unknown')}")
            else:
                result_strings.append(str(result))

        return "\n\n".join(result_strings) if result_strings else "No relevant documentation found."
    except Exception as e:
        return f"Error searching documentation: {str(e)}"


@function_tool
def greet_user(name: str = "User") -> str:
    """Generate a friendly greeting for the user"""
    greetings = [
        f"Hello {name}! I'm here to help you with your questions.",
        f"Hi {name}! How can I assist you today?",
        f"Greetings {name}! Feel free to ask me anything about the documentation."
    ]

    return greetings[0]


@function_tool
async def search_qdrant(query: str) -> str:
    """Search relevant book content from Qdrant"""
    try:
        # Step 1: Get embedding
        query_vector = await embedding_service.create_query_embedding(query)

        # Step 2: Search Qdrant
        results = await qdrant_service.search_documentation(query_vector, limit=5)

        # Step 3: Format results
        result_strings = []
        for result in results:
            result_strings.append(
                f"Content: {result.get('text', '')}\nSource: {result.get('metadata', {}).get('source_file', 'Unknown')}"
            )

        return "\n\n".join(result_strings) if result_strings else "No relevant content found."
    except Exception as e:
        return f"Error searching Qdrant: {str(e)}"