import re
import time
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.config import GROQ_API_KEY, GROQ_MODEL_NAME
from src.retriever import Retriever
from src.nli_detector import NLIDetector
from src.credibility import CredibilityScorer

class PyContraAgent:
    def __init__(self):
        print("🤖 Initializing PyContra Agent...")
        self.retriever = Retriever()
        self.nli = NLIDetector()
        self.scorer = CredibilityScorer()
        
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY, 
            model_name=GROQ_MODEL_NAME,
            temperature=0.1 
        )
        
        # Updated Prompt with Chat History (Memory)
        self.prompt = PromptTemplate(
            input_variables=["chat_history", "query", "context", "conflict_info"],
            template="""You are an expert Python Assistant. 
Answer the user's query using the provided context.

If there is a conflict between sources, prioritize the source with the higher credibility score. 
Explain that there was a conflict, and state which version is correct based on the newer documentation.

Chat History:
{chat_history}

Query: {query}

Context (with Credibility Scores):
{context}

Conflict Info: {conflict_info}

Provide a clear, definitive answer and cite the source version you used.
Answer:"""
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()

    def process_query(self, query: str, chat_history: str = "") -> dict:
        start_time = time.time()
        print(f"\n🔍 User Query: {query}")
        
        # 1. Search
        docs = self.retriever.search(query, top_k=2)
        if len(docs) < 2:
            return {"answer": "Not enough documents found.", "details": None, "metrics": {}}

        doc1, doc2 = docs[0], docs[1]

        # 2. Conflict Check
        conflict_res = self.nli.check_conflict(doc1['text'], doc2['text'])
        
        # 3. Credibility Scoring
        def get_version(metadata):
            source = metadata.get('source', '')
            match = re.search(r'(\d+\.\d+)', source)
            return float(match.group(1)) if match else 0.0

        v1, v2 = get_version(doc1['metadata']), get_version(doc2['metadata'])
        score1, score2 = self.scorer.get_score(version=v1), self.scorer.get_score(version=v2)

        context = f"Source 1 (V{v1}) [Score: {score1:.2f}]: {doc1['text']}\n\nSource 2 (V{v2}) [Score: {score2:.2f}]: {doc2['text']}"
        
        conflict_info = "NO CONFLICT DETECTED."
        if conflict_res['is_conflict']:
            conflict_info = f"⚠️ CONFLICT DETECTED! (Confidence: {conflict_res['score']})."

        # 4. Generate Answer
        final_answer = self.chain.invoke({
            "chat_history": chat_history,
            "query": query,
            "context": context,
            "conflict_info": conflict_info
        })
        
        # Calculate Latency
        latency = round(time.time() - start_time, 2)
        
        return {
            "answer": final_answer,
            "details": {
                "conflict": conflict_res,
                "source_1": {"version": v1, "score": score1, "text": doc1['text']},
                "source_2": {"version": v2, "score": score2, "text": doc2['text']}
            },
            "metrics": {"latency": latency, "model": GROQ_MODEL_NAME}
        }