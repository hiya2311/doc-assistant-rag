from sentence_transformers import SentenceTransformer
import chromadb

# Load model and connect to existing ChromaDB (doesn't recreate anything)
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_or_create_collection(name="support_tickets")

def search(query, n_results=3):
    """Takes a question, returns the most relevant chunks."""
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    return results

if __name__ == "__main__":
    test_query = "My AWS deployment costs are too high, how do I fix it?"
    print(f"\nSearching for: '{test_query}'\n")
    results = search(test_query)
    for i, doc in enumerate(results['documents'][0]):
        print(f"--- Result {i+1} ---")
        print(doc[:300], "...")
        print()