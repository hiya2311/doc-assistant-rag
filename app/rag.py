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

    prompt = f"""You are an IT support assistant. Answer the user's question using ONLY the information in the past support tickets below. Do not use any outside knowledge, even if you know the answer.

If the tickets do not contain relevant information to answer the question, respond with exactly this: "I don't have relevant information in the support ticket database to answer this question." Do not provide any answer beyond that statement.

Past support tickets:
{context}

User question: {query}

Answer using ONLY the tickets above:"""
    
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