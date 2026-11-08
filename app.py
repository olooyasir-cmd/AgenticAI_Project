
import streamlit as st
from langchain_core.messages import AIMessageChunk

from main import create_research_agent


# --------------------------------
# 1. Streamlit page configuration
# --------------------------------

st.set_page_config(
    page_title="Research Agent",
    page_icon="🤖"
)

st.title("Yasir Research Agent 🤖")

st.write(
    "Ask the research agent to find the latest news "
    "and real-time updates."
)


# --------------------------------
# 2. Cache the research agent
# --------------------------------

@st.cache_resource
def get_agent():
    return create_research_agent()


agent = get_agent()


# --------------------------------
# 3. Initialize session cache
# --------------------------------

if "research_cache" not in st.session_state:
    st.session_state.research_cache = {}


# --------------------------------
# 4. User input
# --------------------------------

user_query = st.text_input(
    "Enter your question:",
    placeholder="What is the latest news?"
)


# --------------------------------
# 5. Run research agent
# --------------------------------

if st.button("Run Search"):

    if user_query.strip():

        query_key = user_query.strip().lower()

        st.subheader("Research Agent Response")

        # Check whether the question is cached
        if query_key in st.session_state.research_cache:

            st.info("Retrieved from cache ⚡")

            st.markdown(
                st.session_state.research_cache[query_key]
            )

        else:

            placeholder = st.empty()
            full_response = ""

            with st.spinner("Searching..."):

                for message_chunk, metadata in agent.stream(
                    {"messages": [("human", user_query)]},
                    stream_mode="messages"
                ):

                    # Only display AI-generated text chunks
                    if isinstance(message_chunk, AIMessageChunk):

                        content = message_chunk.content

                        if isinstance(content, str):
                            full_response += content

                        elif isinstance(content, list):
                            for block in content:
                                if (
                                    isinstance(block, dict)
                                    and block.get("type") == "text"
                                ):
                                    full_response += block["text"]

                        placeholder.markdown(
                            full_response + " ▌"
                        )

            # Save completed response
            st.session_state.research_cache[query_key] = full_response

            placeholder.markdown(full_response)

    else:
        st.warning(
            "Please enter a question to run the search agent."
        )


# --------------------------------
# 6. Clear cached answers
# --------------------------------

if st.button("Clear Search Cache"):

    st.session_state.research_cache.clear()

    st.success("Research cache cleared successfully!")
