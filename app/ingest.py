import pandas as pd

# ---------- Load & clean (same as before) ----------
df = pd.read_csv("data/support_tickets.csv")
df_en = df[df['language'] == 'en'].copy()
df_en = df_en.dropna(subset=['answer'])

def build_document(row):
    subject = str(row['subject']) if pd.notna(row['subject']) else ""
    body = str(row['body']) if pd.notna(row['body']) else ""
    answer = str(row['answer']) if pd.notna(row['answer']) else ""
    return f"Subject: {subject}\nQuestion: {body}\nResolution: {answer}"

df_en['document'] = df_en.apply(build_document, axis=1)

# ---------- NEW: Chunking logic ----------
def chunk_text(text, chunk_size=800, overlap=100):
    """
    Splits text into overlapping chunks.
    chunk_size = max characters per chunk
    overlap = characters repeated between chunks (preserves context across the split)
    """
    if len(text) <= chunk_size:
        return [text]  # short enough, no need to split

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap  # move forward, but overlap a bit
    return chunks

# Build a list of chunks, each remembering which original ticket it came from
all_chunks = []
for idx, row in df_en.iterrows():
    ticket_chunks = chunk_text(row['document'])
    for i, chunk in enumerate(ticket_chunks):
        all_chunks.append({
            "chunk_id": f"ticket_{idx}_chunk_{i}",
            "ticket_id": idx,
            "text": chunk,
            "queue": row['queue'],
            "priority": row['priority']
        })

print("Total tickets:", len(df_en))
print("Total chunks created:", len(all_chunks))
print("\n--- Sample chunk ---\n")
print(all_chunks[0])

# Save chunks for the next step (embeddings)
chunks_df = pd.DataFrame(all_chunks)
chunks_df.to_csv("data/chunks.csv", index=False)
print("\nSaved chunks to data/chunks.csv")