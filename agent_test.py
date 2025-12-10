"""
Simple Streamlit app to test RAG Agent connection.
"""

import os
import streamlit as st
from backend.database import RAGDatabase
from backend.agent import RAGAgent
import config

st.title("RAG Agent Test")

api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    help="Enter your OpenAI API key"
)

if not api_key:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

os.environ["OPENAI_API_KEY"] = api_key

db = RAGDatabase(config.DEFAULT_DB_PATH)

if not db.test_connection():
    st.error("❌ Database connection failed. Fix that first.")
    st.stop()

st.success("✅ Database connected")


agent = RAGAgent(db, config.DEFAULT_MODEL, config.DEFAULT_MAX_ITER)

question = st.text_input("Test question", placeholder="Ask a question about your database...")

if not question:
    st.info("Enter a question to test the agent.")
    st.stop()

with st.spinner("Testing agent..."):
    try:
        result = agent.ask(question)
        st.success("✅ Agent working!")
        st.write("**Answer:**", result["answer"])
    except Exception as e:
        st.error(f"❌ Agent failed: {e}")