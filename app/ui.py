import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(__file__))
from rag import generate_answer
from retrieve import search

st.set_page_config(page_title="IT Support Assistant", page_icon="🛠️", layout="centered")

# ---------- Custom CSS ----------
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 {
        color: white !important;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        color: #DBEAFE !important;
        font-size: 1rem;
        margin: 0;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    div[data-testid="stExpander"] {
        border-radius: 10px;
        border: 1px solid #E2E8F0;
    }
    .tech-badge {
        display: inline-block;
        background-color: #EFF6FF;
        color: #2563EB;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="main-header">
    <h1>🛠️ AI-Powered IT Documentation Support Assistant</h1>
    <p>Ask a question and get an answer grounded in real past support tickets — powered by Retrieval-Augmented Generation (RAG)</p>
</div>
""", unsafe_allow_html=True)

# ---------- Example questions ----------
st.write("**✨ Try an example:**")
col1, col2, col3 = st.columns(3)

example_query = None
with col1:
    if st.button("💰 AWS costs too high", use_container_width=True):
        example_query = "My AWS deployment costs are too high, how do I fix it?"
with col2:
    if st.button("🖥️ Server crashing", use_container_width=True):
        example_query = "Server keeps crashing, what should I check?"
with col3:
    if st.button("🔐 Password reset", use_container_width=True):
        example_query = "How do I reset a user's password?"

st.write("")

query = st.text_input(
    "Or ask your own question:",
    value=example_query if example_query else "",
    placeholder="e.g. My AWS deployment costs are too high, how do I fix it?"
)

get_answer_clicked = st.button("🔍 Get Answer", type="primary", use_container_width=True)

if get_answer_clicked and query:
    with st.spinner("🔎 Searching 3,397 support tickets and generating a grounded answer..."):
        answer = generate_answer(query)
        retrieved = search(query, n_results=3)

    st.divider()
    st.subheader("💬 Answer")
    st.info(answer)

    with st.expander("📄 View retrieved support tickets (sources used)"):
        for i, doc in enumerate(retrieved['documents'][0]):
            st.markdown(f"**Source {i+1}:**")
            st.text(doc[:500] + ("..." if len(doc) > 500 else ""))
            st.divider()

# ---------- Footer ----------
st.write("")
st.divider()
st.markdown("""
<div style="text-align: center;">
    <span class="tech-badge">Python</span>
    <span class="tech-badge">sentence-transformers</span>
    <span class="tech-badge">ChromaDB</span>
    <span class="tech-badge">Groq / Llama 3.1</span>
    <span class="tech-badge">Streamlit</span>
</div>
""", unsafe_allow_html=True)