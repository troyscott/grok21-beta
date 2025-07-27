#!/usr/bin/env python3
"""
Test script to verify the changes made to the Grok21 Blackjack Strategy Helper.
This script tests:
1. The fixed file name (basic_strategy.txt)
2. Improved error handling in the RAG chain
3. Edge case handling in strategy lookups
"""

import os
import sys
from strategy_table import get_action
from rag_chain import GrokRagChain

def test_file_exists():
    """Test that the renamed file exists"""
    print("\n--- Testing File Rename ---")
    file_path = "data/documents/basic_strategy.txt"
    if os.path.exists(file_path):
        print(f"✅ File {file_path} exists")
    else:
        print(f"❌ File {file_path} does not exist")

def test_strategy_table():
    """Test the strategy table with valid and invalid inputs"""
    print("\n--- Testing Strategy Table ---")
    
    # Test valid inputs
    test_cases = [
        # hand_type, player_value, dealer_upcard, expected_result
        ("hard", 16, 10, "H"),
        ("soft", 18, 6, "Ds"),
        ("pair", 8, 8, "P"),
    ]
    
    for hand_type, player_value, dealer_upcard, expected in test_cases:
        try:
            result = get_action(hand_type, player_value, dealer_upcard)
            if result == expected:
                print(f"✅ {hand_type} {player_value} vs {dealer_upcard}: {result}")
            else:
                print(f"❌ {hand_type} {player_value} vs {dealer_upcard}: Expected {expected}, got {result}")
        except Exception as e:
            print(f"❌ {hand_type} {player_value} vs {dealer_upcard}: {str(e)}")
    
    # Test edge cases
    edge_cases = [
        # hand_type, player_value, dealer_upcard, should_raise
        ("invalid", 16, 10, True),
        ("hard", 4, 10, True),  # Below valid range
        ("hard", 22, 10, True),  # Above valid range
        ("soft", 12, 10, True),  # Below valid range
        ("soft", 21, 10, True),  # Above valid range
        ("pair", 1, 10, True),   # Below valid range
        ("pair", 12, 10, True),  # Above valid range
        ("hard", 16, 1, True),   # Below valid dealer range
        ("hard", 16, 12, True),  # Above valid dealer range
    ]
    
    for hand_type, player_value, dealer_upcard, should_raise in edge_cases:
        try:
            result = get_action(hand_type, player_value, dealer_upcard)
            if should_raise:
                print(f"❌ {hand_type} {player_value} vs {dealer_upcard}: Expected exception, got {result}")
            else:
                print(f"✅ {hand_type} {player_value} vs {dealer_upcard}: {result}")
        except ValueError as e:
            if should_raise:
                print(f"✅ {hand_type} {player_value} vs {dealer_upcard}: Correctly raised {type(e).__name__}")
            else:
                print(f"❌ {hand_type} {player_value} vs {dealer_upcard}: {str(e)}")
        except Exception as e:
            print(f"❓ {hand_type} {player_value} vs {dealer_upcard}: Unexpected error: {type(e).__name__}: {str(e)}")

def test_rag_chain_validation():
    """Test the input validation in the RAG chain"""
    print("\n--- Testing RAG Chain Input Validation ---")
    
    try:
        rag_chain = GrokRagChain()
        
        # Test invalid hand type
        result = rag_chain.get_response("", "invalid_type", 16, 10)
        if "Invalid hand type" in result:
            print("✅ Invalid hand type correctly detected")
        else:
            print(f"❌ Invalid hand type not detected: {result}")
        
        # Test invalid player value
        result = rag_chain.get_response("", "hard", 30, 10)
        if "Invalid player value" in result:
            print("✅ Invalid player value correctly detected")
        else:
            print(f"❌ Invalid player value not detected: {result}")
        
        # Test invalid dealer upcard
        result = rag_chain.get_response("", "hard", 16, 15)
        if "Invalid dealer upcard" in result:
            print("✅ Invalid dealer upcard correctly detected")
        else:
            print(f"❌ Invalid dealer upcard not detected: {result}")
        
    except Exception as e:
        print(f"❌ Error testing RAG chain validation: {str(e)}")

def main():
    """Run all tests"""
    print("=== Testing Grok21 Blackjack Strategy Helper Changes ===")
    
    # Test file rename
    test_file_exists()
    
    # Test strategy table
    test_strategy_table()
    
    # Test RAG chain validation
    test_rag_chain_validation()
    
    print("\n=== Testing Complete ===")

if __name__ == "__main__":
    main()