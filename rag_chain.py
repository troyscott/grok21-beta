import os
import json
import logging
from typing import Optional
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI as OpenAIClient
import torch
import streamlit as st  # Added for st.secrets

logging.basicConfig(level=logging.INFO)


class GrokRagChain:
    def __init__(self, docs_folder: str = "data/documents", model: str = None,
                 expansion_temp: float = None, response_temp: float = None, max_tokens: int = None):
        device = 'cpu'  # Force CPU
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-large-en-v1.5",
            model_kwargs={'device': device}
        )
        self.vectorstore = self._load_or_create_vectorstore(docs_folder)
        self.grok_client = self._setup_grok_client()
        self.model = model or os.getenv("GROK_MODEL", "grok-3-mini")
        self.expansion_temp = float(expansion_temp or os.getenv("EXPANSION_TEMP", "0.7"))
        self.response_temp = float(response_temp or os.getenv("RESPONSE_TEMP", "0.8"))
        self.max_tokens = int(max_tokens or os.getenv("MAX_TOKENS", "500"))

    def _load_or_create_vectorstore(self, docs_folder: str):
        index_path = "faiss_index"
        if os.path.exists(index_path):
            return FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)

        docs = []
        for filename in os.listdir(docs_folder):
            filepath = os.path.join(docs_folder, filename)
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(filepath)
                docs.extend(loader.load())
            elif filename.endswith(".txt"):
                loader = TextLoader(filepath)
                docs.extend(loader.load())

        if not docs:
            raise ValueError("No documents in data/documents/. Add Blackjack files.")

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        vectorstore.save_local(index_path)
        return vectorstore

    def _setup_grok_client(self):
        api_key = st.secrets.get("XAI_API_KEY", os.getenv("XAI_API_KEY"))  # Use st.secrets for deployment
        if not api_key:
            raise ValueError("XAI_API_KEY not set")
        return OpenAIClient(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )

    def get_response(self, query: str, hand_type: Optional[str] = None, player_value: Optional[int] = None,
                     dealer_upcard: Optional[int] = None) -> str:
        from strategy_table import get_action

        # Fast path: Use heuristic table for hand lookups
        if player_value is not None and dealer_upcard is not None:
            action = get_action(hand_type or "hard", player_value, dealer_upcard)
            explanations = {
                'H': 'Hit: Improves EV against the dealer\'s likely strong hand.',
                'S': 'Stand: Avoids bust risk with a strong enough total.',
                'D': 'Double: Maximizes profit when the dealer is weak (2-6).',
                'Ds': 'Double if allowed, else Stand: Optimizes EV with caution.',
                'P': 'Split: Creates two hands for better win potential.'
            }
            return f"Optimal Basic Strategy action: {action}. {explanations.get(action, 'Action based on optimal play.')}"

        # RAG path: Use Grok for chat queries
        try:
            expansion_prompt = f"Expand this Blackjack query into 2-3 related sub-queries for better retrieval. Output as JSON list: [\"subquery1\", \"subquery2\", \"subquery3\"]: {query}"
            expansion_response = self.grok_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": expansion_prompt}],
                temperature=self.expansion_temp
            ).choices[0].message.content
            try:
                expanded_queries = json.loads(expansion_response)
            except json.JSONDecodeError:
                logging.warning("Failed to parse expansion response; falling back to split.")
                expanded_queries = [q.strip() for q in expansion_response.split("\n") if q.strip()]
            logging.info(f"Expanded queries: {expanded_queries}")

            contexts = set()
            for eq in expanded_queries:
                results = self.vectorstore.similarity_search(eq, k=2)
                contexts.update(doc.page_content for doc in results)

            full_context = '\n\n'.join(contexts)[:10000] + '...' if len('\n\n'.join(contexts)) > 10000 else '\n\n'.join(
                contexts)
            full_prompt = f"Context: {full_context}\n\nQuery: {query}\nAnswer as Grok with clear reasoning:"
            response = self.grok_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=self.response_temp,
                max_tokens=self.max_tokens
            ).choices[0].message.content
            return response

        except Exception as e:
            logging.error(f"Error in get_response: {e}")
            return f"An error occurred: {str(e)}. Please try again or check the API key."