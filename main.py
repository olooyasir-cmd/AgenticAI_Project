
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env
load_dotenv()

# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL"),
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    max_retries=3,
    timeout=120,
)

# Initialize Tavily Search
tavily_search = TavilySearch(
    max_results=3,
    topic="news",
)

# Define the search tool
@tool
def search_news(query: str) -> str:
    """
    Search for the latest news articles related to a given query.
    """
    results = tavily_search.invoke({"query": query})
    return str(results)


# Create the research agent
def create_research_agent():
    return create_agent(
        model=llm,
        tools=[search_news],
        system_prompt=(
            #"I am a Jamaican research assistant, respond to me in Jamaican Patois. "
            "You are a research assistant. "
            "Use the search_news tool to find accurate and current information. "
            "Summarize the search results clearly. "
            "Do not invent facts."
        ),
    )

#Creating Streaming 
def create_streaming_research():
    return create_agent(
        model=llm,
        tools=[search_news],
        system_prompt=(
            "You are a research assistant. "
            "Use the search_news tool to find accurate and current information. "
            "Summarize the search results clearly. "
            "Do not invent facts."
        ),
        streaming=True,
    )

# Run the agent
if __name__ == "__main__":
    agent = create_research_agent()

    try:
        response = agent.invoke({
            "messages": [
                ("user", "What is the latest news about the Tesla Roadster?")
            ]
        })

        print("\nAI Response:")
        print(response["messages"][-1].content[0]["text"])

    except Exception as e:
        print("\nAgent execution failed.")
        print(f"Error: {e}")
