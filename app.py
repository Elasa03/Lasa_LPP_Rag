# =============================================================================
# Streamlit Application for RAG Assistant
# =============================================================================
# This is the user interface. It imports our backend modules and handles:
# - Page layout and configuration
# - User input (chat, sidebar settings)
# - Displaying responses and sources
# - Session state management
# =============================================================================

import streamlit as st
import os
from backend.database import RAGDatabase
from backend.agent import RAGAgent
import config

# -----------------------------------------------------------------------------
# Page Configuration (must be first Streamlit command)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="World War 1 RAG Assistant",
    page_icon="📖",
    layout="wide"
)
st.markdown("""
<style>

    /* ------------------------------ */
    /* GLOBAL APP BACKGROUND          */
    /* ------------------------------ */
    [data-testid="stAppViewContainer"] {
        /* Faded trench-map parchment */
        background: radial-gradient(circle at top left, #f5edd8 0%, #e7ddc4 35%, #d7c9a8 60%, #c4b28a 100%);
        color: #1f2933 !important;
    }

    /* Slight paper texture illusion using overlay */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image:
            radial-gradient(circle at 1px 1px, rgba(0,0,0,0.05) 1px, transparent 0);
        background-size: 8px 8px;
        opacity: 0.25;
        z-index: -1;
    }

    /* Make default text dark and readable on parchment */
    html, body, [data-testid="stAppViewContainer"] * {
        color: #1f2933;
        font-family: "Georgia", "Times New Roman", serif;
    }

    /* ------------------------------ */
    /* SIDEBAR - LEATHER / FIELD DESK */
    /* ------------------------------ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #3b3427 0%, #2b251d 100%) !important;
        border-right: 2px solid #5b4b33;
    }

    [data-testid="stSidebar"] * {
        color: #f5f5f4 !important;
    }

    /* Sidebar headers */
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        font-family: "Georgia", "Times New Roman", serif;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.9rem;
        color: #f0e7d5 !important;
    }

    /* ------------------------------ */
    /* TITLES                         */
    /* ------------------------------ */
    h1 {
        color: #3b3222 !important;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 2.1rem;
        border-bottom: 2px solid #8b5a2b;
        padding-bottom: 0.3rem;
        margin-bottom: 0.5rem;
    }

    h2, h3 {
        color: #4a3b25 !important;
    }

    /* ------------------------------ */
    /* CHAT MESSAGES (MAP CARDS)      */
    /* ------------------------------ */
    /* Generic chat message container */
    div[data-testid="stChatMessage"] {
        border-radius: 10px;
        padding: 0.75rem 0.9rem;
        margin-bottom: 0.6rem;
        border: 1px solid #b69d72;
        background: rgba(248, 241, 220, 0.9);
        box-shadow: 0 2px 4px rgba(0,0,0,0.18);
    }

    /* Try to differentiate user vs assistant a bit using order */
    /* User: slightly greener card */
    div[data-testid="stChatMessage"]:nth-of-type(odd) {
        background: rgba(214, 204, 173, 0.98);
        border-left: 4px solid #4f6b3b;
    }

    /* Assistant: more neutral parchment */
    div[data-testid="stChatMessage"]:nth-of-type(even) {
        background: rgba(247, 239, 217, 0.98);
        border-left: 4px solid #8b5a2b;
    }

    /* ------------------------------ */
    /* EXPANDERS (Sources, Examples)  */
    /* ------------------------------ */
    details {
        background-color: rgba(244, 235, 214, 0.95) !important;
        border: 1px solid #b69d72 !important;
        border-radius: 6px !important;
        padding: 4px 6px !important;
        margin-top: 0.4rem !important;
    }

    details > summary {
        color: #3b3222 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }

    /* ------------------------------ */
    /* TEXT AREAS (source passages)   */
    /* ------------------------------ */
    textarea, .stTextArea textarea {
        background-color: #f8f1dd !important;
        color: #1f2933 !important;
        border: 1px solid #b69d72 !important;
        border-radius: 6px !important;
        font-family: "Courier New", monospace;
        font-size: 0.85rem;
    }

    /* ------------------------------ */
    /* BUTTONS - FIELD-ORDER LOOK     */
    /* ------------------------------ */
    button {
        background-color: #4a5b3b !important;      /* field green */
        color: #f5f5f4 !important;
        border-radius: 999px !important;
        border: 1px solid #2f3a26 !important;
        padding: 0.35rem 0.9rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        text-transform: none !important;
    }

    button:hover {
        background-color: #5f7249 !important;
        color: #ffffff !important;
        border-color: #2f3a26 !important;
    }

    /* Example question buttons: make them look like stamped labels */
    .stButton button {
        box-shadow: 0 2px 0 rgba(0,0,0,0.25);
    }

    /* ------------------------------ */
    /* INPUTS & SLIDERS               */
    /* ------------------------------ */
    .stTextInput > div > input,
    .stNumberInput input {
        background-color: #f8f1dd !important;
        color: #1f2933 !important;
        border-radius: 4px !important;
        border: 1px solid #b69d72 !important;
    }

    .stSlider > div > div > div {
        background-color: #8b5a2b !important; /* trench-brown slider track */
    }

    /* ------------------------------ */
    /* LINKS                          */
    /* ------------------------------ */
    a {
        color: #7b3f00 !important;  /* rust/brown */
        text-decoration: underline dotted !important;
    }

    a:hover {
        color: #a8550c !important;
    }

    /* ------------------------------ */
    /* CHAT INPUT BOX                 */
    /* ------------------------------ */
    [data-baseweb="textarea"] textarea {
        background-color: #f8f1dd !important;
        border-radius: 8px !important;
        border: 1px solid #b69d72 !important;
    }

</style>
""", unsafe_allow_html=True)




# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
# IMPORTANT: Streamlit reruns this entire file every time the user:
# - Types a message
# - Clicks a button  
# - Moves a slider
#
# Without session state, our chat history would vanish on every interaction.
# st.session_state store a dictionary on session information that should persist
# through user interactions.
# 
# Pattern: if 'key' not in st.session_state: st.session_state.key = default
# -----------------------------------------------------------------------------

# Chat history - list of {"role": "user"/"assistant", "content": "..."}
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Database path from sidebar
if 'db_path' not in st.session_state:
    st.session_state.db_path = config.DEFAULT_DB_PATH

# Number of results to retrieve
if 'top_k' not in st.session_state:
    st.session_state.top_k = config.DEFAULT_TOP_K

# Database instance (expensive to create, so we cache it)
if 'database' not in st.session_state:
    st.session_state.database = None


# -----------------------------------------------------------------------------
# Sidebar - User Configuration
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # TO DO: API Key input
    # Make sure the user can hide their input
    api_key = st.text_input("OpenAI API Key", type = "password", help = "Enter your OpenAI API Key") #Make sure words in textbox are hidden
    
    # TO DO: Database path input via config.py
    db_path = st.text_input("Database Path", value = config.DEFAULT_DB_PATH, help = "Path to your DuckDB vector database")
    
    # Store in session state
    st.session_state.db_path = db_path
    
    # TO DO: Top K results with an interactive slider bar
    top_k = st.slider("Results per Query", min_value = 3, max_value = 20, value = config.DEFAULT_TOP_K, help = "Number of chunks to retreive per search")
    # Store in session state
    st.session_state.top_k = top_k
    
    # TO DO: Model selection dropdown menu
    model_choice = st.selectbox("LLM model", config.AVAILABLE_MODELS, index = 0)
    
    # TO DO: Create max_iter slider
    # Max iterations for tool calls
    max_iter = st.slider("Max Tools Calls", min_value = 1, max_value = 5, value = config.DEFAULT_MAX_ITER, help = "Maximum number of database queries per question")
    
    st.divider()
    
    # TO DO: Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # TO DO: Update for your project # Talk about your project
    st.markdown("""
    ### About
    This RAG assistant answers questions about the First World War using:
    - Historians World War 1 video transcripts
    - Historical Documents
    - Historians Analysis of the War
    - Semantic search with embeddings
    """)

# -----------------------------------------------------------------------------
# Main App Header
# -----------------------------------------------------------------------------
st.title("🪖 World War 1 RAG Assistant")
st.markdown("Ask questions about the TOPIC and get AI-powered answers based on curated content.")

st.markdown("""
<div style="text-align:center; padding:10px;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/2/2e/WWI_British_Army_insignia_%28simplified%29.png" 
         width="110" style="margin-bottom: -10px;">
    <h2 style="margin-top: -5px; font-family: 'Georgia'; color:#3b3222;">
        Western Front Intelligence Assistant
    </h2>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Database Connection
# -----------------------------------------------------------------------------
# Recreate database instance if path changed from default in case multiple duckdb files
if not st.session_state.database or st.session_state.database.db_path != db_path:
    st.session_state.database = RAGDatabase(db_path)

# Test and display connection status
if not st.session_state.database.test_connection():
    st.error(f"❌ Database not found at: `{db_path}`")
    st.info("Please update the database path in the sidebar.")
    if not os.path.exists(db_path):
        st.stop() # Stop execution here - can't continue without database
else:
    st.success(f"✅ Database connected: `{db_path}`")

# -----------------------------------------------------------------------------
# API Key Check
# -----------------------------------------------------------------------------
if not api_key:
    st.warning("⚠️ Please enter your OpenAI API key in the sidebar to continue.")
    st.stop()

# Set the API key as environment variable (OpenAI client reads from here)
os.environ["OPENAI_API_KEY"] = api_key

# -----------------------------------------------------------------------------
# Display Chat History
# -----------------------------------------------------------------------------
# Loop through all previous messages and display them
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show sources for assistant messages if available
        if message["role"] == "assistant" and message.get("sources"):

            # Creates expander bar and allows user to view sources
            with st.expander(f"View Sources ({len(message['sources'])} passages retrieved)"):
                
                # Loops over source number and content
                for i, source in enumerate(message["sources"], 1):
                    st.markdown(f"**Source {i}** (Similarity: {source['similarity']:.3f})")
                    st.text_area(
                        f"Passage {i}",
                        source["text"],
                        height=150,
                        key=f"source_{id(message)}_{i}",
                        label_visibility="collapsed"
                    )
                    st.divider()

# -----------------------------------------------------------------------------
# Chat Input and Response Generation
# -----------------------------------------------------------------------------
# st.chat_input returns None until user submits, then returns their text
# The := (walrus operator) assigns AND checks in one line

if prompt := st.chat_input("Ask a question about TOPIC..."):
    
    # TO DO: Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # TO DO: Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Searching database and generating answer..."):
            try:
                # TO DO: Initialize Agent
                agent = RAGAgent(db = st.session_state.database,
                                 max_iter = max_iter,
                                 model_name = model_choice)
                
                # Get answer
                result = agent.ask(prompt)
                response = result["answer"]
                sources = result["sources"]
                
                st.markdown(response)
                
                # Display sources immediately
                if sources:
                    with st.expander(f"📚 View Sources ({len(sources)} passages retrieved)"):
                        for i, source in enumerate(sources, 1):
                            st.markdown(f"**Source {i}** (Similarity: {source['similarity']:.3f})")
                            st.text_area(
                                f"Passage {i}",
                                source["text"],
                                height=150,
                                key=f"source_new_{i}",
                                label_visibility="collapsed"
                            )
                            if i < len(sources):
                                st.divider()
                
                # Add to history with sources
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "sources": sources
                })
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "sources": []
                })

# TO DO: Example questions in an expander
with st.expander("💡 Example Questions"):
    examples = [
        "How did World War 1 start?.",
        "What where the allied and Axis Powers?",
        "Give me an outline for a reaserch paper on World War 1?",
        "Give me some facts about the war?",
        "Was there really a ceasefire on christmas 1914?"
    ]
    
    for example in examples:
        if st.button(example, key=example):
            # Simulate entering the question
            st.session_state.messages.append({"role": "user", "content": example})
            st.rerun()
