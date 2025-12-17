from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ChatRequest(BaseModel):
    """
    Represents a user's request to the chatbot system
    """
    message: str = Field(..., description="The user's question or input text")
    thread_id: Optional[str] = Field(None, description="Identifier for conversation context persistence")


class SelectedTextChatRequest(BaseModel):
    """
    Represents a user's request with additional selected text context
    """
    message: str = Field(..., description="The user's question about the selected text")
    selected_text: str = Field(..., description="The text content selected by the user")
    thread_id: Optional[str] = Field(None, description="Identifier for conversation context persistence")


class Source(BaseModel):
    """
    Represents a source citation in the chat response
    """
    text: str = Field(..., description="The content of the documentation chunk")
    score: float = Field(..., description="Relevance score from vector similarity search")
    metadata: Dict[str, Any] = Field(..., description="Additional information about the source")


class ChatResponse(BaseModel):
    """
    Represents the system's response to a user's chat request
    """
    answer: str = Field(..., description="The agent's response to the user's question")
    thread_id: Optional[str] = Field(None, description="Identifier for conversation context persistence")
    sources: Optional[List[Source]] = Field(None, description="List of source citations if applicable")


class HealthResponse(BaseModel):
    """
    Represents the system's health status
    """
    status: str = Field(..., description="Health status indicator")
    message: str = Field(..., description="Descriptive message about the health status")