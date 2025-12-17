import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from api.models import ChatRequest, SelectedTextChatRequest, ChatResponse
from agents_folder.rag_agent import RAGAgent, GreetingAgent, SelectedTextAgent, MainRouterAgent
from services.qdrant_service import QdrantService
from services.embedding_service import EmbeddingService


@pytest.fixture
def mock_qdrant_service():
    """Mock Qdrant service for testing"""
    service = AsyncMock(spec=QdrantService)
    service.search_documentation = AsyncMock(return_value=[
        {
            "text": "This is a test document",
            "score": 0.9,
            "metadata": {
                "source_file": "test.md",
                "relative_path": "docs/test.md",
                "full_path": "/path/to/docs/test.md"
            },
            "size": 22
        }
    ])
    return service


@pytest.fixture
def mock_embedding_service():
    """Mock embedding service for testing"""
    service = AsyncMock(spec=EmbeddingService)
    service.create_query_embedding = AsyncMock(return_value=[0.1, 0.2, 0.3])
    return service


@pytest.mark.asyncio
async def test_rag_agent_process_query():
    """Test RAG agent processing query"""
    # Create a mock tools registry
    mock_tools = AsyncMock()
    mock_tools.search_documentation = AsyncMock(return_value={
        "success": True,
        "results": [
            {
                "text": "This is a test document",
                "score": 0.9,
                "metadata": {
                    "source_file": "test.md",
                    "relative_path": "docs/test.md",
                    "full_path": "/path/to/docs/test.md"
                }
            }
        ],
        "query": "test query"
    })

    # Create RAG agent instance and mock the tools
    rag_agent = RAGAgent()
    rag_agent.tools = mock_tools

    # Mock the OpenAI client
    import agents_folder.rag_agent
    agents.rag_agent.client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = MagicMock()
    mock_response.choices[0].message.content = "Test answer"
    agents.rag_agent.client.chat.completions.create.return_value = mock_response

    # Test the process_query method
    result = await rag_agent.process_query("test query", "test_thread")

    assert result["answer"] == "Test answer"
    assert len(result["sources"]) == 1
    assert result["thread_id"] == "test_thread"


@pytest.mark.asyncio
async def test_greeting_agent_process_greeting():
    """Test greeting agent processing greeting"""
    # Create a mock tools registry
    mock_tools = AsyncMock()
    mock_tools.greet_user = AsyncMock(return_value={
        "greeting": "Hello User! I'm here to help you with your questions.",
        "name": "User"
    })

    # Create greeting agent instance and mock the tools
    greeting_agent = GreetingAgent()
    greeting_agent.tools = mock_tools

    # Test the process_greeting method
    result = await greeting_agent.process_greeting("Hello", "test_thread")

    assert "Hello" in result["answer"]
    assert result["thread_id"] == "test_thread"


@pytest.mark.asyncio
async def test_selected_text_agent_process_query():
    """Test selected text agent processing query"""
    # Mock the OpenAI client
    import agents_folder.rag_agent
    agents.rag_agent.client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = MagicMock()
    mock_response.choices[0].message.content = "Test answer based on selected text"
    agents.rag_agent.client.chat.completions.create.return_value = mock_response

    # Create selected text agent instance
    selected_text_agent = SelectedTextAgent()

    # Test the process_query method
    result = await selected_text_agent.process_query(
        "What does this text say?",
        "This is the selected text content",
        "test_thread"
    )

    assert "Test answer based on selected text" in result["answer"]
    assert result["thread_id"] == "test_thread"


@pytest.mark.asyncio
async def test_main_router_agent_route_request_greeting():
    """Test main router agent routing greeting request"""
    # Create a mock tools registry
    mock_tools = AsyncMock()
    mock_tools.greet_user = AsyncMock(return_value={
        "greeting": "Hello User! I'm here to help you with your questions.",
        "name": "User"
    })

    # Create main router agent instance
    router_agent = MainRouterAgent()

    # Mock the greeting agent's tools
    router_agent.greeting_agent.tools = mock_tools

    # Test routing a greeting request
    result = await router_agent.route_request("hello", "test_thread")

    assert "Hello" in result["answer"]
    assert result["thread_id"] == "test_thread"


@pytest.mark.asyncio
async def test_main_router_agent_route_request_rag():
    """Test main router agent routing RAG request"""
    # Create a mock tools registry for RAG
    mock_tools = AsyncMock()
    mock_tools.search_documentation = AsyncMock(return_value={
        "success": True,
        "results": [
            {
                "text": "This is a test document",
                "score": 0.9,
                "metadata": {
                    "source_file": "test.md",
                    "relative_path": "docs/test.md",
                    "full_path": "/path/to/docs/test.md"
                }
            }
        ],
        "query": "test query"
    })

    # Create main router agent instance
    router_agent = MainRouterAgent()

    # Mock the RAG agent's tools
    router_agent.rag_agent.tools = mock_tools

    # Mock the OpenAI client
    import agents_folder.rag_agent
    agents.rag_agent.client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = MagicMock()
    mock_response.choices[0].message.content = "Test RAG answer"
    agents.rag_agent.client.chat.completions.create.return_value = mock_response

    # Test routing a RAG request
    result = await router_agent.route_request("What is this?", "test_thread")

    assert "Test RAG answer" in result["answer"]
    assert result["thread_id"] == "test_thread"


@pytest.mark.asyncio
async def test_main_router_agent_route_request_selected_text():
    """Test main router agent routing selected text request"""
    # Create main router agent instance
    router_agent = MainRouterAgent()

    # Mock the OpenAI client
    import agents_folder.rag_agent
    agents.rag_agent.client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = MagicMock()
    mock_response.choices[0].message.content = "Test selected text answer"
    agents.rag_agent.client.chat.completions.create.return_value = mock_response

    # Test routing a selected text request
    result = await router_agent.route_request(
        "What does this text say?",
        "test_thread",
        "This is the selected text content"
    )

    assert "Test selected text answer" in result["answer"]
    assert result["thread_id"] == "test_thread"


def test_chat_request_model():
    """Test ChatRequest model validation"""
    request = ChatRequest(message="Test message", thread_id="test_thread")

    assert request.message == "Test message"
    assert request.thread_id == "test_thread"


def test_selected_text_chat_request_model():
    """Test SelectedTextChatRequest model validation"""
    request = SelectedTextChatRequest(
        message="Test message",
        selected_text="Selected text",
        thread_id="test_thread"
    )

    assert request.message == "Test message"
    assert request.selected_text == "Selected text"
    assert request.thread_id == "test_thread"


def test_chat_response_model():
    """Test ChatResponse model validation"""
    response = ChatResponse(
        answer="Test answer",
        thread_id="test_thread",
        sources=[]
    )

    assert response.answer == "Test answer"
    assert response.thread_id == "test_thread"
    assert response.sources == []