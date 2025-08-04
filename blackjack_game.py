"""
Blackjack strategy helper - NOT a game, but a companion for online blackjack
Uses fast heuristic tables + RAG/Grok for learning
"""


import sys

try:
    import pysqlite3
    sys.modules["sqlite3"] = pysqlite3
    sys.modules["sqlite"] = pysqlite3
except ImportError:
    # pysqlite3 not available, use standard sqlite3
    pass


import streamlit as st
from rag_chain import GrokRagChain
from strategy_table import get_action

def get_strategy_advice(player_total, dealer_upcard, hand_type="hard"):
    """
    Get blackjack strategy advice - the core function of this app
    
    Args:
        player_total: Player's hand total 
        dealer_upcard: Dealer's visible card
        hand_type: "hard", "soft", or "pair"
    
    Returns:
        Strategy advice using heuristic tables + explanations
    """
    
    # Convert Ace=1 to Ace=11 for consistent table lookup
    dealer_key = 11 if dealer_upcard == 1 else dealer_upcard
    
    try:
        # Directly use the strategy table for lookups without initializing RAG chain
        action = get_action(hand_type, player_total, dealer_key)
        
        # Explanations for each action
        explanations = {
            'H': 'Hit: Improves EV against the dealer\'s likely strong hand.',
            'S': 'Stand: Avoids bust risk with a strong enough total.',
            'D': 'Double: Maximizes profit when the dealer is weak (2-6).',
            'Ds': 'Double if allowed, else Stand: Optimizes EV with caution.',
            'P': 'Split: Creates two hands for better win potential.'
        }
        
        return f"Optimal Basic Strategy action: {action}. {explanations.get(action, 'Action based on optimal play.')}"
        
    except Exception as e:
        return f"Error getting strategy advice: {str(e)}"

def ask_grok_question(question):
    """
    Ask Grok a learning question about blackjack strategy
    This uses the RAG system to search documents + generate responses
    """
    if not question or not question.strip():
        return "Please enter a question about blackjack strategy."
        
    try:
        # Add logging to track what's happening
        import logging
        logging.info(f"Starting Grok question: {question[:50]}...")
        
        rag_chain = GrokRagChain()
        logging.info("RAG chain initialized successfully")
        
        # Use RAG path - provide question, no hand parameters  
        response = rag_chain.get_response(query=question)
        logging.info("Got response from RAG chain")
        
        return response
        
    except Exception as e:
        # Log the full error details
        import logging
        logging.error(f"Error in ask_grok_question: {type(e).__name__}: {str(e)}")
        return f"Error asking Grok: {str(e)}"

def handle_grok_interface():
    """
    Complete Grok question interface with proper state management
    Call this function in your Streamlit app where you want the Grok interface
    """
    # Initialize session state
    if 'grok_response' not in st.session_state:
        st.session_state.grok_response = ""
    if 'grok_question' not in st.session_state:
        st.session_state.grok_question = ""
    if 'grok_loading' not in st.session_state:
        st.session_state.grok_loading = False
    
    st.header("🤖 Ask Grok About Blackjack Strategy")
    st.markdown("Get detailed explanations about blackjack strategy decisions and rules.")
    
    # Question input
    question = st.text_area(
        "Your question:",
        value=st.session_state.grok_question,
        height=100,
        placeholder="E.g., Why should I hit on 16 against dealer's 10?",
        help="Ask about specific hands, general strategy, or blackjack rules"
    )
    
    # Button row
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ask_button = st.button(
            "🤖 Ask Grok", 
            key="ask_grok_button",
            disabled=st.session_state.grok_loading,
            use_container_width=True
        )
    
    with col2:
        clear_button = st.button(
            "Clear", 
            key="clear_grok_button",
            disabled=st.session_state.grok_loading
        )
    
    # Handle button clicks
    if ask_button:
        if question and question.strip():
            st.session_state.grok_question = question
            st.session_state.grok_loading = True
        else:
            st.warning("Please enter a question first.")
    
    if clear_button:
        st.session_state.grok_response = ""
        st.session_state.grok_question = ""
        st.session_state.grok_loading = False

    
    # Handle the actual API call if loading
    if st.session_state.grok_loading:
        with st.spinner('🤖 Asking Grok... This may take a few seconds.'):
            response = ask_grok_question(st.session_state.grok_question)
            st.session_state.grok_response = response
            st.session_state.grok_loading = False

    
    # Display response
    if st.session_state.grok_response:
        st.markdown("---")
        st.markdown("### 🤖 Grok's Response:")
        
        # Display the response in a nice container
        with st.container():
            st.markdown(st.session_state.grok_response)
        
        # Show the question that was asked
        with st.expander("📝 Your Question"):
            st.markdown(f"*{st.session_state.grok_question}*")

def simple_grok_interface():
    """
    Simplified version without complex state management
    Use this if you prefer a simpler approach
    """
    st.header("🤖 Ask Grok About Blackjack Strategy")
    
    question = st.text_input(
        "Ask your question:",
        placeholder="Why should I hit on 16 against dealer's 10?"
    )
    
    if st.button("🤖 Ask Grok"):
        if question:
            with st.spinner('🤖 Thinking...'):
                response = ask_grok_question(question)
            
            st.markdown("### Response:")
            st.markdown(response)
        else:
            st.warning("Please enter a question.")