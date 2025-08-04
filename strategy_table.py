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

# Updated pairs table to use totals instead of individual card values
pairs_table = {
    4: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},  # 2-2 (total 4)
    6: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},  # 3-3 (total 6)
    8: {2: 'H', 3: 'H', 4: 'H', 5: 'P', 6: 'P', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},  # 4-4 (total 8)
    10: {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'H', 11: 'H'}, # 5-5 (total 10, treat as hard 10)
    12: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'}, # 6-6 (total 12)
    14: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'H', 9: 'H', 10: 'H', 11: 'H'}, # 7-7 (total 14)
    16: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'P', 9: 'P', 10: 'P', 11: 'P'}, # 8-8 (total 16)
    18: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'S', 8: 'P', 9: 'P', 10: 'S', 11: 'S'}, # 9-9 (total 18)
    20: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'}, # 10-10 (total 20)
    22: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'P', 9: 'P', 10: 'P', 11: 'P'}  # A-A (total 22)
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
        player_value: Player's hand total (all hand types now use totals)
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
    
    # Validate dealer_upcard first
    if dealer_upcard < 2 or dealer_upcard > 11:
        raise ValueError(f"Invalid dealer upcard: {dealer_upcard}. Must be between 2 and 11 (where 11 represents Ace)")
    
    # Validate player_value range based on hand type
    if hand_type_lower == 'hard':
        if player_value < 5 or player_value > 21:
            raise ValueError(f"Invalid hard hand total: {player_value}. Must be between 5 and 21")
    elif hand_type_lower == 'soft':
        if player_value < 13 or player_value > 20:
            raise ValueError(f"Invalid soft hand total: {player_value}. Must be between 13 and 20")
    elif hand_type_lower == 'pair':
        # Valid pair totals: 4, 6, 8, 10, 12, 14, 16, 18, 20, 22
        valid_pair_totals = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
        if player_value not in valid_pair_totals:
            raise ValueError(f"Invalid pair total: {player_value}. Valid pair totals are: 4(2-2), 6(3-3), 8(4-4), 10(5-5), 12(6-6), 14(7-7), 16(8-8), 18(9-9), 20(10-10), 22(A-A)")
    
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
        raise ValueError(f"Hand total {player_value} is bust - no strategy needed")
    
    # Get actions from table
    actions = table.get(player_value)
    if actions is None:
        raise ValueError(f"No strategy found for {hand_type} hand total {player_value}. Please check your input and try again.")
    
    # Normalize dealer upcard (Ace = 11)
    dealer_key = dealer_upcard if dealer_upcard <= 10 else 11
    
    # Get action from the specific dealer upcard
    action = actions.get(dealer_key)
    if action is None:
        raise ValueError(f"No strategy found for {hand_type} {player_value} vs dealer {dealer_upcard}. Please check your input and try again.")
    
    return action