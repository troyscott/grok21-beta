import os

import sys

try:
    import pysqlite3
    sys.modules["sqlite3"] = pysqlite3
    sys.modules["sqlite"] = pysqlite3
except ImportError:
    # pysqlite3 not available, use standard sqlite3
    pass

import json
import logging
from typing import Optional
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma  # Changed from FAISS to Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI as OpenAIClient
import streamlit as st

logging.basicConfig(level=logging.INFO)


class GrokRagChain:
    def __init__(self, docs_folder: str = "data/documents", model: str = None,
                 expansion_temp: float = None, response_temp: float = None, max_tokens: int = None):
        device = 'cpu'  # Force CPU for Streamlit Cloud compatibility
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-large-en-v1.5",
            model_kwargs={'device': device}
        )
        self.vectorstore = self._load_or_create_vectorstore(docs_folder)
        self.grok_client = self._setup_grok_client()
        
        # Get settings from Streamlit secrets first, then environment variables
        self.model = model or st.secrets.get("GROK_MODEL", os.getenv("GROK_MODEL", "grok-3-mini"))
        self.expansion_temp = float(expansion_temp or st.secrets.get("EXPANSION_TEMP", os.getenv("EXPANSION_TEMP", "0.7")))
        self.response_temp = float(response_temp or st.secrets.get("RESPONSE_TEMP", os.getenv("RESPONSE_TEMP", "0.8")))
        self.max_tokens = int(max_tokens or st.secrets.get("MAX_TOKENS", os.getenv("MAX_TOKENS", "500")))

    def _load_or_create_vectorstore(self, docs_folder: str):
        persist_directory = "chroma_db"  # Changed from faiss_index to chroma_db
        
        # Create new index
        if not os.path.exists(docs_folder):
            st.error(f"Documents folder '{docs_folder}' not found. Please ensure it exists with PDF/TXT files.")
            raise ValueError(f"Documents folder '{docs_folder}' not found.")
        
        docs = []
        for filename in os.listdir(docs_folder):
            filepath = os.path.join(docs_folder, filename)
            try:
                if filename.endswith(".pdf"):
                    loader = PyPDFLoader(filepath)
                    docs.extend(loader.load())
                elif filename.endswith(".txt"):
                    loader = TextLoader(filepath)
                    docs.extend(loader.load())
            except Exception as e:
                logging.warning(f"Failed to load {filepath}: {e}")

        if not docs:
            raise ValueError(f"No readable documents found in {docs_folder}/. Add Blackjack PDF or TXT files.")

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        # Use Chroma instead of FAISS
        vectorstore = Chroma.from_documents(
            chunks, 
            self.embeddings,
            persist_directory=persist_directory
        )
        
        return vectorstore

    def _setup_grok_client(self):
        # Try Streamlit secrets first, then environment variables
        api_key = st.secrets.get("XAI_API_KEY") or os.getenv("XAI_API_KEY")
        
        if not api_key:
            raise ValueError("XAI_API_KEY not found in Streamlit secrets or environment variables. Please add it to your app's secrets.")
        
        return OpenAIClient(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )

    def get_response(self, query: str, hand_type: Optional[str] = None, player_value: Optional[int] = None,
                     dealer_upcard: Optional[int] = None) -> str:
        from strategy_table import get_action

        # Validate input parameters
        if hand_type is not None and hand_type.lower() not in ["hard", "soft", "pair"]:
            return f"Invalid hand type: {hand_type}. Must be 'hard', 'soft', or 'pair'."
        
        if player_value is not None and (player_value < 2 or player_value > 21):
            return f"Invalid player value: {player_value}. Must be between 2 and 21."
        
        if dealer_upcard is not None and dealer_upcard not in range(2, 12):
            return f"Invalid dealer upcard: {dealer_upcard}. Must be between 2 and 11 (where 11 represents Ace)."

        # RAG path: Use Grok for chat queries
        if not query.strip() and (player_value is None or dealer_upcard is None):
            return "Please provide a question about blackjack strategy."

        # Fast path: Use heuristic table for hand lookups
        if player_value is not None and dealer_upcard is not None:
            try:
                # For pairs, convert total to individual card value
                if hand_type and hand_type.lower() == "pair":
                    # Convert pair total to individual card value
                    if player_value % 2 != 0 and player_value != 21:  # Odd totals except 21 (A-A)
                        return f"Invalid pair total: {player_value}. Pair totals must be even (except A-A = 21)."
                    
                    if player_value == 21:  # A-A pair
                        pair_value = 11
                    else:
                        pair_value = player_value // 2
                    
                    # Validate pair value range
                    if pair_value < 2 or pair_value > 11:
                        return f"Invalid pair: {player_value}. Valid pairs: 4(2-2), 6(3-3), 8(4-4), 10(5-5), 12(6-6), 14(7-7), 16(8-8), 18(9-9), 20(10-10), 21(A-A)."
                    
                    action = get_action(hand_type, pair_value, dealer_upcard)
                else:
                    action = get_action(hand_type or "hard", player_value, dealer_upcard)
                
                explanations = {
                    'H': 'Hit: Improves EV against the dealer\'s likely strong hand.',
                    'S': 'Stand: Avoids bust risk with a strong enough total.',
                    'D': 'Double: Maximizes profit when the dealer is weak (2-6).',
                    'Ds': 'Double if allowed, else Stand: Optimizes EV with caution.',
                    'P': 'Split: Creates two hands for better win potential.'
                }
                return f"Optimal Basic Strategy action: {action}. {explanations.get(action, 'Action based on optimal play.')}"
            except Exception as e:
                logging.error(f"Error in strategy lookup: {e}")
                return f"Error finding strategy: {str(e)}. Please check your input values and try again."
        
        # Maximum retries for API calls
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Step 1: Query expansion
                try:
                    expansion_prompt = f"Expand this Blackjack query into 2-3 related sub-queries for better retrieval. Output as JSON list: [\"subquery1\", \"subquery2\", \"subquery3\"]: {query}"
                    expansion_response = self.grok_client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": expansion_prompt}],
                        temperature=self.expansion_temp
                    ).choices[0].message.content
                    
                    expanded_queries = json.loads(expansion_response)
                    if not isinstance(expanded_queries, list) or not expanded_queries:
                        raise ValueError("Invalid expansion format")
                        
                except json.JSONDecodeError:
                    logging.warning("Failed to parse expansion response; using original query.")
                    expanded_queries = [query]
                except ValueError as e:
                    logging.warning(f"Invalid expansion format: {e}; using original query.")
                    expanded_queries = [query]
                except Exception as e:
                    logging.warning(f"Query expansion failed: {e}; using original query.")
                    expanded_queries = [query]
                
                logging.info(f"Expanded queries: {expanded_queries}")

                # Step 2: Context retrieval
                contexts = set()
                retrieval_failures = 0
                
                for eq in expanded_queries:
                    try:
                        results = self.vectorstore.similarity_search(eq, k=2)
                        if results:
                            contexts.update(doc.page_content for doc in results)
                        else:
                            logging.warning(f"No results found for query: {eq}")
                    except Exception as e:
                        logging.warning(f"Search failed for query '{eq}': {e}")
                        retrieval_failures += 1
                
                # If all retrievals failed, provide a fallback
                if retrieval_failures == len(expanded_queries):
                    logging.error("All context retrievals failed")
                    return "I'm having trouble accessing my knowledge base right now. Please try a different question or try again later."
                
                # If we have no context but some retrievals succeeded, the query might be unrelated to blackjack
                if not contexts:
                    return "I couldn't find relevant information about that. Please ask a question related to blackjack strategy."

                full_context = '\n\n'.join(contexts)
                if len(full_context) > 10000:
                    full_context = full_context[:10000] + '...'
                
                # Step 3: Generate response
                full_prompt = f"Context: {full_context}\n\nQuery: {query}\nAnswer as Grok with clear reasoning:"
                response = self.grok_client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": full_prompt}],
                    temperature=self.response_temp,
                    max_tokens=self.max_tokens
                ).choices[0].message.content
                
                return response

            except (ConnectionError, TimeoutError) as e:
                # Network-related errors - retry
                retry_count += 1
                logging.warning(f"Network error (attempt {retry_count}/{max_retries}): {e}")
                if retry_count >= max_retries:
                    return "I'm having trouble connecting to my knowledge service. Please check your internet connection and try again later."
                
            except Exception as e:
                # For other errors, log and return a user-friendly message
                error_type = type(e).__name__
                logging.error(f"Error in get_response ({error_type}): {e}")
                
                if "API key" in str(e) or "authentication" in str(e).lower():
                    return "Authentication error. Please check your API key configuration."
                elif "rate limit" in str(e).lower() or "quota" in str(e).lower():
                    return "I've reached my usage limit. Please try again in a few minutes."
                else:
                    return f"An unexpected error occurred. Please try a different question or try again later. Error type: {error_type}"