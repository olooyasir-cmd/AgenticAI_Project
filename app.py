
import streamlit as st
from langchain_core.messages import AIMessageChunk

from main import create_research_agent


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Yasir Research Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. PROFESSIONAL CSS DESIGN
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #07111F,
        #0A1628,
        #0D1B2E
    );
    color: #EAF2FF;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: #081321;
    border-right: 1px solid #1B2D44;
}

[data-testid="stSidebar"] * {
    color: #DCE8F7;
}

h1, h2, h3 {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}

p {
    color: #A9BCD3;
    line-height: 1.7;
}

.brand {
    color: #48CAE4;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 3px;
}

.hero-title {
    color: #FFFFFF;
    font-size: 34px;
    font-weight: 800;
}

.hero-description {
    color: #A9BCD3;
    font-size: 15px;
}

div[data-testid="stTextInput"] input {
    background: #0D1B2E !important;
    color: #FFFFFF !important;
    border: 1px solid #263D59 !important;
    border-radius: 12px !important;
    min-height: 50px;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #48CAE4 !important;
    box-shadow: 0 0 0 2px rgba(72,202,228,0.15);
}

div.stButton > button {
    background: linear-gradient(
        135deg,
        #00B4D8,
        #0077B6
    );
    color: white;
    border: none;
    border-radius: 12px;
    min-height: 48px;
    font-weight: 700;
    transition: 0.3s;
}

div.stButton > button:hover {
    background: #48CAE4;
    color: #FFFFFF;
    transform: translateY(-2px);
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: #10233A;
    border: 1px solid #263D59;
    border-radius: 16px;
}

hr {
    border-color: #263D59 !important;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

.custom-footer {
    text-align: center;
    color: #8197B2;
    font-size: 12px;
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 24px;
    }

    .block-container {
        padding: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("# 🤖")

    st.markdown(

        "<p class='brand'>AI RESEARCH PLATFORM</p>",
        unsafe_allow_html=True
    )

    st.markdown("## Yasir Research Agent")

    st.caption(
        "Intelligent research. Real-time insights. "
        "Smarter decisions."
    )

    st.divider()

    st.markdown("### 🧭 Navigation")

    st.info("🔎 Research Assistant")

    st.divider()

    st.markdown("### ⚙️ Platform Features")

    st.markdown("""
    🌐 Real-time news research

    🧠 AI-powered analysis

    ⚡ Smart response caching

    💬 Streaming AI responses

    🔍 Intelligent search
    """)

    st.divider()

    st.markdown("### 🟢 System Status")

    st.success("Research Agent Ready")

    st.caption("Powered by LangChain & Streamlit")

    st.divider()

    st.caption("Version 1.0.0")


# ============================================================
# 4. MAIN HEADER
# ============================================================

#st.markdown(
#    "<p class='brand'>AI-POWERED RESEARCH PLATFORM</p>",
#    unsafe_allow_html=True
#)

with st.container(border=True):

    st.markdown(
        "<h1 class='hero-title'>Yasir Research Agent 🤖</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class='hero-description'>
        Your intelligent AI research assistant for discovering
        the latest news, analyzing information, and accessing
        real-time updates from the web.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.success("AI RESEARCH SYSTEM ACTIVE")

st.write(
    "Ask your research agent a question and receive "
    "intelligent, AI-generated insights."
)

st.divider()


# ============================================================
# 5. CACHE RESEARCH AGENT
# ============================================================

@st.cache_resource
def get_agent():
    return create_research_agent()


agent = get_agent()


# ============================================================
# 6. INITIALIZE SESSION CACHE
# ============================================================

if "research_cache" not in st.session_state:
    st.session_state.research_cache = {}


# ============================================================
# 7. RESEARCH WORKSPACE
# ============================================================

st.markdown(
    "<p class='brand'>RESEARCH WORKSPACE</p>",
    unsafe_allow_html=True
)

user_query = st.text_input(
    "Enter your question:",
    placeholder="What is in your mind?"
)


# ============================================================
# 8. ACTION BUTTONS
# ============================================================

col1, col2 = st.columns([2, 1])

with col1:

    run_search = st.button(
        "🚀 Run Research",
        use_container_width=True
    )

with col2:

    clear_cache = st.button(
        "🗑️ Clear Cache",
        use_container_width=True
    )


# ============================================================
# 9. RUN RESEARCH AGENT
# ============================================================

if run_search:

    if user_query.strip():

        query_key = user_query.strip().lower()

        st.divider()

        st.markdown("### 🔎 Research Results")

        st.markdown("#### Research Agent Response")

        # Check whether the question is cached

        if query_key in st.session_state.research_cache:

            st.info("⚡ Retrieved from cache")

            with st.container(border=True):

                st.markdown(
                    st.session_state.research_cache[query_key]
                )

        else:

            placeholder = st.empty()

            full_response = ""

            try:

                with st.spinner(
                    "Research agent is searching the web..."
                ):

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

                st.session_state.research_cache[
                    query_key
                ] = full_response

                placeholder.markdown(full_response)

            except Exception as e:

                placeholder.empty()

                st.error(
                    f"Research error: {str(e)}"
                )

    else:

        st.warning(
            "Please enter a question to run the search agent."
        )


# ============================================================
# 10. CLEAR SEARCH CACHE
# ============================================================

if clear_cache:

    st.session_state.research_cache.clear()

    st.success(
        "Research cache cleared successfully!"
    )


# ============================================================
# 11. FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="custom-footer">
        Built with ❤️ using Streamlit and LangChain
        <br><br>
        <strong>Yasir Research Agent</strong>
        | AI-Powered Research Platform
    </div>
    """,
    unsafe_allow_html=True
)
