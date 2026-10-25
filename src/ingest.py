import requests
from bs4 import BeautifulSoup
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import CHROMA_DB_DIR, EMBEDDING_MODEL_NAME

URLS = {
    "Python_3.6_Docs": "https://docs.python.org/3.6/tutorial/datastructures.html",
    "Python_3.10_Docs": "https://docs.python.org/3.10/tutorial/datastructures.html"
}

def fetch_and_extract_text(url):
    print(f"Downloading: {url}...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Main content-ah mattum edukkanum, so navigation bar ellam remove panrom
    main_content = soup.find('div', {'role': 'main'})
    if main_content:
        return main_content.get_text(separator=' ', strip=True)
    return soup.get_text(separator=' ', strip=True)

def main():
    print("Starting Data Ingestion...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len
    )

    # 3. ChromaDB Setup 
    print("Connecting to ChromaDB...")
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
    
    # Embedding function 
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME
    )
    
    # Collection create 
    collection = chroma_client.get_or_create_collection(
        name="python_docs",
        embedding_function=sentence_transformer_ef
    )

    # 4. Download & Save
    for doc_name, url in URLS.items():
        text = fetch_and_extract_text(url)
        chunks = text_splitter.split_text(text)
        
        print(f"Saving {len(chunks)} chunks for {doc_name}...")
        
        # Add to database
        collection.add(
            documents=chunks,
            metadatas=[{"source": doc_name, "url": url} for _ in chunks],
            ids=[f"{doc_name}_chunk_{i}" for i in range(len(chunks))]
        )
        print(f"✅ {doc_name} successfully saved!")

    print(f"Total documents in DB: {collection.count()}")
    print("Ingestion Complete!")

if __name__ == "__main__":
    main()