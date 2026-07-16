from retrieve import search
import re

test_questions = [
    ("My AWS deployment costs are too high, how do I fix it?", "AWS/cloud costs"),
    ("Server keeps crashing, what should I check?", "server stability"),
    ("How do I reset a user's password?", "password/account access"),
    ("Database connection keeps failing", "database issues"),
    ("How do I fix slow application performance?", "performance"),
    ("VPN is not connecting for remote employees", "network/VPN"),
    ("Email server is down", "email/communication systems"),
    ("How to set up two-factor authentication?", "security/authentication"),
    ("Software license has expired", "licensing"),
    ("Printer is not responding on the network", "hardware/printing"),
]

def extract_subject(text):
    """Pulls just the Subject line for clearer evaluation."""
    match = re.search(r"Subject:\s*(.+)", text)
    return match.group(1).strip() if match else "(no subject found)"

print(f"{'='*70}")
print("RETRIEVAL EVALUATION")
print(f"{'='*70}\n")

relevant_count = 0

for query, expected_topic in test_questions:
    results = search(query, n_results=3)
    print(f"Query: {query}")
    print(f"Expected topic: {expected_topic}")
    print("Top 3 retrieved subjects:")
    for i, doc in enumerate(results['documents'][0]):
        subject = extract_subject(doc)
        print(f"  {i+1}. {subject}")
    print("-" * 70)

print("\nGo through each query above and count how many had at least")
print("one clearly relevant subject in the top 3 results.")