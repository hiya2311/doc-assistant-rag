import os
from groq import Groq
from retrieve import search

try:
    import streamlit as st
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def generate_answer(query, n_results=3):
    """
    Full RAG pipeline:
    1. Retrieve relevant chunks (the 'R' in RAG)
    2. Build a prompt with that context
    3. Send to Groq LLM to generate a natural answer (the 'AG' in RAG)
    """
    # Step 1: Retrieve
    results = search(query, n_results=n_results)
    retrieved_chunks = results['documents'][0]

    # Step 2: Build context from retrieved chunks
    context = "\n\n---\n\n".join(retrieved_chunks)

    prompt = f"""You are an IT support assistant. Use the following past support tickets to answer the user's question. If the tickets don't contain relevant info, say so honestly.

Past support tickets:
{context}

User question: {query}

Answer clearly and concisely, based on the tickets above:"""

    # Step 3: Generate answer using Groq
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

# ---------- Test it ----------
if __name__ == "__main__":
    test_query = "My AWS deployment costs are too high, how do I fix it?"
    print(f"\nQuestion: {test_query}\n")

    answer = generate_answer(test_query)
    print("Answer:\n")
    print(answer)