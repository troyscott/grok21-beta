# Full Basic Strategy heuristic tables for multi-deck (4-8), dealer stands on soft 17 (S17), DAS allowed, no surrender.
# Actions: 'H' (Hit), 'S' (Stand), 'D' (Double if allowed, else Hit), 'Ds' (Double if allowed, else Stand), 'P' (Split)
# Dealer upcard: 2-10 (int), 11 for Ace.

hard_table = {
    5: {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    6: {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    7: {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    8: {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    9: {2: 'H', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    10: {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'H', 11: 'H'},
    11: {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'D', 11: 'H'},
    12: {2: 'H', 3: 'H', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    13: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    14: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    15: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    16: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
    17: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
    18: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
    19: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
    20: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
    21: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'}
}

soft_table = {
    13: {2: 'H', 3: 'H', 4: 'H', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},  # A2
    14: {2: 'H', 3: 'H', 4: 'H', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},  # A3
    15: {2: 'H', 3: 'H', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},  # A4
    16: {2: 'H', 3: 'H', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},  # A5
    17: {2: 'H', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},  # A6
    18: {2: 'Ds', 3: 'Ds', 4: 'Ds', 5: 'Ds', 6: 'Ds', 7: 'S', 8: 'S', 9: 'H', 10: 'H', 11: 'H'},  # A7
    19: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},  # A8
    20: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'}   # A9
}

pairs_table = {
    2: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},  # 2-2
    3: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},  # 3-3
    4: {2: 'H', 3: 'H', 4: 'H', 5: 'P', 6: 'P', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},  # 4-4
    5: {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'H', 11: 'H'},  # 5-5 (treat as 10)
    6: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},  # 6-6
    7: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},  # 7-7
    8: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'P', 9: 'P', 10: 'P', 11: 'P'},  # 8-8
    9: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'S', 8: 'P', 9: 'P', 10: 'S', 11: 'S'},  # 9-9
    10: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'}, # 10-10
    11: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'P', 9: 'P', 10: 'P', 11: 'P'}  # A-A
}

def get_action_text(action_code: str) -> str:
    """Convert action codes to simple, obvious words"""
    action_map = {
        'H': 'Hit',
        'S': 'Pass',
        'D': 'Double',
        'Ds': 'Double or Pass',
        'P': 'Split'
    }
    return action_map.get(action_code, action_code)

def get_action(hand_type: str, player_value: int, dealer_upcard: int) -> str:
    """
    Get the optimal blackjack action based on hand type, player value, and dealer upcard.
    
    Args:
        hand_type: Type of hand - "hard", "soft", or "pair"
        player_value: Player's hand total (2-21)
        dealer_upcard: Dealer's visible card (2-11, where 11 represents Ace)
        
    Returns:
        Action code: 'H' (Hit), 'S' (Stand), 'D' (Double), 'Ds' (Double if allowed, else Stand), 'P' (Split)
        
    Raises:
        ValueError: If inputs are invalid or out of range
    """
    # Validate inputs
    if not isinstance(hand_type, str):
        raise ValueError(f"Hand type must be a string, got {type(hand_type).__name__}")
    
    if not isinstance(player_value, int):
        raise ValueError(f"Player value must be an integer, got {type(player_value).__name__}")
    
    if not isinstance(dealer_upcard, int):
        raise ValueError(f"Dealer upcard must be an integer, got {type(dealer_upcard).__name__}")
    
    # Normalize hand_type to lowercase
    hand_type_lower = hand_type.lower()
    
    # Validate hand_type
    if hand_type_lower not in ['hard', 'soft', 'pair']:
        raise ValueError(f"Invalid hand type: {hand_type}. Must be 'hard', 'soft', or 'pair'")
    
    # Validate player_value range based on hand type
    if hand_type_lower == 'hard':
        if player_value < 5 or player_value > 21:
            raise ValueError(f"Invalid hard hand value: {player_value}. Must be between 5 and 21")
    elif hand_type_lower == 'soft':
        if player_value < 13 or player_value > 20:
            raise ValueError(f"Invalid soft hand value: {player_value}. Must be between 13 and 20")
    elif hand_type_lower == 'pair':
        if player_value < 2 or player_value > 11:
            raise ValueError(f"Invalid pair value: {player_value}. Must be between 2 and 11")
    
    # Validate dealer_upcard
    if dealer_upcard < 2 or dealer_upcard > 11:
        raise ValueError(f"Invalid dealer upcard: {dealer_upcard}. Must be between 2 and 11")
    
    # Get the appropriate table
    table = {
        'hard': hard_table,
        'soft': soft_table,
        'pair': pairs_table
    }.get(hand_type_lower)
    
    # Handle edge cases with special rules
    if hand_type_lower == 'hard' and player_value < 5:
        return 'H'  # Always hit very low hands
    
    if hand_type_lower == 'hard' and player_value > 21:
        return 'BUST'  # Bust
    
    # Get actions from table
    actions = table.get(player_value, {})
    
    # Normalize dealer upcard (Ace = 11)
    dealer_key = dealer_upcard if dealer_upcard <= 10 else 11
    
    # Get action with fallback to hit
    return actions.get(dealer_key, 'H')