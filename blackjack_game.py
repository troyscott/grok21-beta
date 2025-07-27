"""
Blackjack strategy helper - NOT a game, but a companion for online blackjack
Uses fast heuristic tables + RAG/Grok for learning
"""

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
    
    try:
        rag_chain = GrokRagChain()
        
        # Use RAG path - provide question, no hand parameters
        response = rag_chain.get_response(query=question)
        
        return response
        
    except Exception as e:
        return f"Error asking Grok: {str(e)}"