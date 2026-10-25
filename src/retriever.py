import chromadb
from chromadb.utils import embedding_functions
from src.config import CHROMA_DB_DIR, EMBEDDING_MODEL_NAME

class Retriever:
    def __init__(self):
        print("Initializing Retriever...")
        self.chroma_client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
        
        # Same embedding model we used during ingestion
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL_NAME
        )
        
        # Load the collection
        self.collection = self.chroma_client.get_collection(
            name="python_docs",
            embedding_function=self.embedding_fn
        )

    def search(self, query: str, top_k: int = 4):
        """Searches the vector database for relevant chunks."""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        # Format the output nicely
        retrieved_docs = []
        if results['documents'] and len(results['documents']) > 0:
            for i in range(len(results['documents'][0])):
                retrieved_docs.append({
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
                
        return retrieved_docs

# --- Test block ---
if __name__ == "__main__":
    retriever = Retriever()
    test_query = "Does Python dictionary maintain insertion order?"
    print(f"\nSearching for: '{test_query}'\n")
    
    docs = retriever.search(test_query)
    for idx, doc in enumerate(docs):
        print(f"--- Result {idx + 1} ---")
        print(f"Source: {doc['metadata']['source']}")
        print(f"Text: {doc['text'][:300]}...\n") # Print first 300 characters