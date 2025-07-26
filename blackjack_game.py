"""
Blackjack strategy helper - NOT a game, but a companion for online blackjack
Uses fast heuristic tables + RAG/Grok for learning
"""

from rag_chain import GrokRagChain

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
        # Initialize RAG chain - this handles both:
        # 1. Fast heuristic table lookup (when player_value + dealer_upcard provided)  
        # 2. RAG/Grok explanations (when query provided)
        rag_chain = GrokRagChain()
        
        # Use heuristic path - empty query triggers table lookup
        response = rag_chain.get_response(
            query="",
            hand_type=hand_type,
            player_value=player_total,
            dealer_upcard=dealer_key
        )
        
        return response
        
    except Exception as e:
        return f"Error getting strategy advice: {str(e)}"

def ask_grok_question(question):
    """
    Ask Grok a learning question about blackjack strategy
    This uses the RAG system to search documents + generate responses
    """
    
    try:
        rag_chain = GrokRagChain()
        
        # Use RAG path - provide question, no hand parameters
        response = rag_chain.get_response(query=question)
        
        return response
        
    except Exception as e:
        return f"Error asking Grok: {str(e)}"