import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(__file__))

# Check if the vector database already exists; if not, build it
if not os.path.exists("data/chroma_db"):
    with st.spinner("First-time setup: building the search index... (takes 1-2 minutes)"):
        import build_index  # running this file executes the indexing code

from rag import generate_answer
from retrieve import search

st.set_page_config(page_title="IT Support Assistant", page_icon="🛠️")

st.title("🛠️ AI-Powered IT Documentation Support Assistant")
st.write("Ask a question about IT support issues (AWS, deployments, servers, etc.) and get an answer grounded in real past support tickets.")

query = st.text_input("Ask your question:", placeholder="e.g. My AWS deployment costs are too high, how do I fix it?")

if st.button("Get Answer") and query:
    with st.spinner("Searching past tickets and generating answer..."):
        answer = generate_answer(query)
        retrieved = search(query, n_results=3)

    st.subheader("Answer")
    st.write(answer)

    with st.expander("📄 View retrieved support tickets (sources used)"):
        for i, doc in enumerate(retrieved['documents'][0]):
            st.markdown(f"**Source {i+1}:**")
            st.text(doc[:500] + ("..." if len(doc) > 500 else ""))
            st.divider()