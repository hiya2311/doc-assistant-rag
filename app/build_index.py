from sentence_transformers import SentenceTransformer
import chromadb
import pandas as pd

print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Loading chunks...")
chunks_df = pd.read_csv("data/chunks.csv")
chunks_df['queue'] = chunks_df['queue'].fillna("Unknown")
chunks_df['priority'] = chunks_df['priority'].fillna("Unknown")

print("Setting up ChromaDB...")
client = chromadb.PersistentClient(path="data/chroma_db")

# Delete old collection if it exists, so we don't get duplicates
try:
    client.delete_collection(name="support_tickets")
except:
    pass

collection = client.get_or_create_collection(name="support_tickets")

print("Generating embeddings and storing them...")
batch_size = 100
for i in range(0, len(chunks_df), batch_size):
    batch = chunks_df.iloc[i:i+batch_size]
    texts = batch['text'].tolist()
    ids = batch['chunk_id'].tolist()
    metadatas = batch[['ticket_id', 'queue', 'priority']].to_dict('records')
    embeddings = model.encode(texts).tolist()
    collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)
    print(f"Processed {i + len(batch)} / {len(chunks_df)} chunks")

print("\nDone! Total chunks stored in ChromaDB:", collection.count())