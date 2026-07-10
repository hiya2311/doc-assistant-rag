import streamlit as st
import sys
import os

# Make sure Python can find rag.py in the same folder
sys.path.append(os.path.dirname(__file__))
from rag import generate_answer

st.set_page_config(page_title="IT Support Assistant", page_icon="🛠️")

st.title("🛠️ AI-Powered IT Documentation Support Assistant")
st.write("Ask a question about IT support issues (AWS, deployments, servers, etc.) and get an answer grounded in real past support tickets.")

query = st.text_input("Ask your question:", placeholder="e.g. My AWS deployment costs are too high, how do I fix it?")

if st.button("Get Answer") and query:
    with st.spinner("Searching past tickets and generating answer..."):
        answer = generate_answer(query)
    st.subheader("Answer")
    st.write(answer)