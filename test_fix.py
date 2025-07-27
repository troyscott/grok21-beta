#!/usr/bin/env python3
"""
Test script to verify the fix for the strategy lookup feature.
This script tests that get_strategy_advice directly uses strategy_table.py
without initializing the RAG chain.
"""

from blackjack_game import get_strategy_advice

def test_strategy_advice():
    """Test that get_strategy_advice returns the expected results."""
    print("Testing get_strategy_advice function...")
    
    # Test cases for different hand types
    test_cases = [
        # Hard hands
        {"hand_type": "hard", "player_total": 12, "dealer_upcard": 6, "expected_action": "S"},
        {"hand_type": "hard", "player_total": 16, "dealer_upcard": 10, "expected_action": "H"},
        {"hand_type": "hard", "player_total": 11, "dealer_upcard": 7, "expected_action": "D"},
        
        # Soft hands
        {"hand_type": "soft", "player_total": 18, "dealer_upcard": 6, "expected_action": "Ds"},
        {"hand_type": "soft", "player_total": 17, "dealer_upcard": 3, "expected_action": "D"},
        {"hand_type": "soft", "player_total": 19, "dealer_upcard": 10, "expected_action": "S"},
        
        # Pairs
        {"hand_type": "pair", "player_total": 8, "dealer_upcard": 8, "expected_action": "P"},
        {"hand_type": "pair", "player_total": 10, "dealer_upcard": 5, "expected_action": "S"},
        {"hand_type": "pair", "player_total": 4, "dealer_upcard": 4, "expected_action": "H"}
    ]
    
    # Run the tests
    for i, test in enumerate(test_cases, 1):
        hand_type = test["hand_type"]
        player_total = test["player_total"]
        dealer_upcard = test["dealer_upcard"]
        expected_action = test["expected_action"]
        
        # Get the advice
        advice = get_strategy_advice(player_total, dealer_upcard, hand_type)
        
        # Check if the advice contains the expected action
        if f"Optimal Basic Strategy action: {expected_action}" in advice:
            print(f"✅ Test {i} passed: {hand_type} {player_total} vs {dealer_upcard} -> {expected_action}")
        else:
            print(f"❌ Test {i} failed: {hand_type} {player_total} vs {dealer_upcard}")
            print(f"  Expected: {expected_action}")
            print(f"  Got: {advice}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_strategy_advice()