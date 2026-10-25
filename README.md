# 🐍 PyContraRAG: Contradiction-Aware RAG with Agentic Arbitration

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

## 📖 Overview
Standard Retrieval-Augmented Generation (RAG) systems often fail when the underlying corpus contains **contradictory information**. For example, Python documentation across different versions (e.g., Python 3.6 vs. Python 3.10) frequently introduces breaking changes and direct contradictions (e.g., dictionary insertion order guarantees). 

**PyContraRAG** is an advanced RAG system designed specifically for evolving technical documentation. It goes beyond simple retrieval by actively detecting contradictions between sources, scoring their credibility using a traditional Machine Learning model, and utilizing a LangChain agent to arbitrate and provide the most accurate, version-appropriate answer.

## 💡 The Solution (How it works)
1. **Retrieval**: Fetches top-k relevant chunks from ChromaDB based on the user query.
2. **Conflict Detection**: A DeBERTa NLI (Natural Language Inference) model analyzes the retrieved chunks to detect if they contradict each other.
3. **Credibility Scoring**: An XGBoost regression model scores the trustworthiness of the documents (e.g., prioritizing Python 3.10 over 3.6).
4. **Agentic Arbitration**: A LangChain Agent (using Llama 3 via Groq) reasons through the conflict, weighs the ML scores, and generates a final, grounded answer with source citations.

## 🏗️ Architecture Flow
```text
[ User Query ]
      │
      ▼
[ 1. ChromaDB Retriever ] ──> Fetches top-k docs (e.g., Python 3.6 & 3.10)
      │
      ▼
[ 2. NLI Detector ] ────────> DeBERTa Model checks for Contradiction
      │
      ▼
[ 3. Credibility Scorer ] ──> XGBoost Model assigns Trust Scores
      │
      ▼
[ 4. LangChain Agent ] ─────> LLM arbitrates and writes final answer




   Layer                        Technology Used
Frontend UI           Streamlit (Custom Glassmorphism Theme)
Agent Framework       LangChain
LLM Engine            Llama 3 (via Groq API)
Conflict Detection    HuggingFace Transformers (DeBERTa-v3-small)
ML Scoring            XGBoost Regressor
Vector Database       ChromaDB
Embeddings            Sentence-Transformers (all-MiniLM-L6-v2)




How to Run Locally:

1. Clone the repository:

git clone https://github.com/your-username/PyContraRAG.git
cd PyContraRAG

2. Create a virtual environment & install dependencies:

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

3. Set up Environment Variables:
Create a .env file in the root directory and add your free Groq API key:

GROQ_API_KEY=your_gsk_key_here

4. Ingest Python Documentation (RAG Setup):

python -m src.ingest

5. Train the Credibility ML Model:

python -m src.credibility

6. Run the Streamlit Application:

python -m streamlit run app/main.py




PROJECT STRUCTURE:

contra-rag/
├── app/                  # Streamlit frontend & Custom CSS
├── src/                  # Backend logic (RAG, ML, Agent)
│   ├── agent.py          # LangChain Orchestrator
│   ├── credibility.py    # XGBoost ML Scorer
│   ├── nli_detector.py   # DeBERTa Conflict Detector
│   └── retriever.py      # ChromaDB Vector Search
├── data/                 # Raw & Processed Data
├── models/               # Saved ML Model (.pkl)
└── requirements.txt      # Dependencies




AUTHOR:

Subashini E | https://github.com/subashini340 | https://www.linkedin.com/in/subashini-e-bba5a132a/
