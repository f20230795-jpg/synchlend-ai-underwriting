import chromadb
import json
import os

# Initialize persistent Chroma client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Safely get or create the collection without embedding function conflicts
collection = chroma_client.get_or_create_collection(name="underwriting_policies")

def init_vector_db():
    if collection.count() == 0 and os.path.exists("policy_rules.json"):
        with open("policy_rules.json", "r") as f:
            rules = json.load(f)
        
        documents = [r["rule_text"] for r in rules]
        metadatas = [{"category": r["category"]} for r in rules]
        ids = [r["id"] for r in rules]
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print("Vector Database successfully initialized.")

def query_policies(user_notes: str, top_k: int = 1):
    results = collection.query(
        query_texts=[user_notes],
        n_results=top_k
    )
    extracted_docs = results.get('documents', [[]])[0]
    return extracted_docs[0] if extracted_docs else "Standard Underwriting Policy Applies."