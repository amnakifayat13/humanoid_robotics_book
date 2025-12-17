"""
Main entry point for the OpenAI Agents RAG Chatbot API
"""
import uvicorn
from api.main import app
from agents_folder.rag_agent import main_agent


def run_server():
    """
    Run the FastAPI server
    """
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )


def run_agent():
    """
    Run the main agent directly
    """
    print("Starting the main agent...")
    print("Agent name:", main_agent.name)
    print("Agent instructions:", main_agent.instructions)
    print("Agent is ready to handle requests!")

    # Simple interaction loop
    while True:
        try:
            user_input = input("\nEnter your query (or 'quit' to exit): ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            # Process the user input with the main agent
            print(f"Processing: {user_input}")
            # Note: Actual agent processing would depend on the specific Agents SDK implementation
            print("Agent response: [Response would appear here based on the agent's processing]")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "agent":
        run_agent()
    else:
        run_server()