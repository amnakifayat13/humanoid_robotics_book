from agents import Agent
from .tools import search_qdrant, greet_user,search_documentation


# Define the Book RAG Agent following the example pattern
# rag_agent = Agent(
#     name="Book RAG Agent",
#     instructions="""
#     You are an expert assistant for the Humanoid Robotics book.
#     Use the search_qdrant tool to retrieve relevant content
#     before answering.
#     Answer ONLY using retrieved content.
#     """,
#     tools=[search_qdrant],
# )


# # Define the Greeting Agent
# greeting_agent = Agent(
#     name="Greeting Assistant",
#     instructions="""
#     You are a friendly chatbot assistant. When users greet you, respond with a warm and welcoming message.
#     Keep the greeting simple and friendly, and invite them to ask questions about the documentation.
#     Use the greet_user tool to generate appropriate greetings.
#     """,
#     tools=[greet_user],
# )


# # Define the Selected Text Agent
# selected_text_agent = Agent(
#     name="Selected Text Assistant",
#     instructions="""
#     You are a helpful assistant that answers questions based only on the provided text context.
#     Do not use any external knowledge or documentation - only answer based on the text provided by the user.
#     If the answer cannot be found in the provided text, acknowledge this limitation.
#     """,
#     tools=[search_documentation],
# )


# Define the Main Agent with function tools instead of nested agents
main_agent = Agent(
    name="Main Agent",
    instructions="""
    You are an expert assistant for the Humanoid Robotics book.
    Use the search_qdrant tool to retrieve relevant content before answering.
    Answer ONLY using retrieved content.
    If a user is greeting you, respond warmly and invite them to ask questions about the book.
    If a user provides specific text and asks questions about it, answer based on that text.
    For questions about the Humanoid Robotics book content, use the search_qdrant tool to find relevant information.
    """,
    tools=[search_qdrant, greet_user,search_documentation],  # Use function tools instead of nested agents
)