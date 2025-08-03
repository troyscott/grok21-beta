#!/usr/bin/env python3
"""
Comprehensive test suite for the Grok21 Blackjack Strategy Helper.
This test focuses on systematically testing the strategy table combinations
and ensuring all scenarios work correctly.
"""

import pytest
from strategy_table import get_action, get_action_text
from blackjack_game import get_strategy_advice

class TestStrategyTable:
    """Test the strategy table lookup functionality"""
    
    def test_hard_hands_basic_scenarios(self):
        """Test common hard hand scenarios"""
        test_cases = [
            # (player_total, dealer_upcard, expected_action)
            (8, 6, 'H'),   # Always hit 8 or less
            (9, 6, 'D'),   # Double 9 vs 3-6
            (10, 5, 'D'),  # Double 10 vs 2-9
            (11, 7, 'D'),  # Double 11 vs 2-10
            (12, 6, 'S'),  # Stand 12 vs 4-6
            (16, 10, 'H'), # Hit 16 vs 7-A
            (17, 11, 'S'), # Stand 17+
        ]
        
        for player_total, dealer_upcard, expected in test_cases:
            result = get_action('hard', player_total, dealer_upcard)
            assert result == expected, f"Hard {player_total} vs {dealer_upcard}: expected {expected}, got {result}"
    
    def test_soft_hands_basic_scenarios(self):
        """Test common soft hand scenarios"""
        test_cases = [
            # (player_total, dealer_upcard, expected_action)
            (13, 6, 'D'),   # A2 vs 5-6
            (17, 6, 'D'),   # A6 vs 3-6
            (18, 6, 'Ds'),  # A7 vs 2-6 (Double or Stand)
            (18, 9, 'H'),   # A7 vs 9-10-A
            (19, 10, 'S'),  # A8+ always stand
        ]
        
        for player_total, dealer_upcard, expected in test_cases:
            result = get_action('soft', player_total, dealer_upcard)
            assert result == expected, f"Soft {player_total} vs {dealer_upcard}: expected {expected}, got {result}"
    
    def test_pair_scenarios(self):
        """Test pair splitting scenarios"""
        test_cases = [
            # (pair_total, dealer_upcard, expected_action)
            (4, 7, 'P'),   # 2-2 (total 4) vs 2-7
            (16, 11, 'P'), # 8-8 (total 16) always split
            (18, 7, 'S'),  # 9-9 (total 18) vs 7, 10, A
            (20, 5, 'S'),  # 10-10 (total 20) never split
            (22, 6, 'P'),  # A-A (total 22) always split
        ]
        
        for pair_total, dealer_upcard, expected in test_cases:
            result = get_action('pair', pair_total, dealer_upcard)
            assert result == expected, f"Pair total {pair_total} vs {dealer_upcard}: expected {expected}, got {result}"
    
    def test_edge_cases(self):
        """Test boundary conditions"""
        # Hard hands boundaries
        assert get_action('hard', 5, 2) == 'H'    # Minimum hard hand
        assert get_action('hard', 21, 11) == 'S'  # Maximum hard hand
        
        # Soft hands boundaries  
        assert get_action('soft', 13, 2) == 'H'   # Minimum soft hand (A-2)
        assert get_action('soft', 20, 11) == 'S'  # Maximum soft hand (A-9)
        
        # Pairs boundaries
        assert get_action('pair', 2, 2) == 'P'    # Minimum pair (2-2)
        assert get_action('pair', 11, 11) == 'P'  # Maximum pair (A-A)
    
    def test_all_dealer_upcards(self):
        """Test that all dealer upcards (2-11) work"""
        for dealer_upcard in range(2, 12):  # 2-11
            # Test with a common scenario
            result = get_action('hard', 16, dealer_upcard)
            assert result in ['H', 'S'], f"Invalid action for hard 16 vs {dealer_upcard}: {result}"
    
    def test_invalid_inputs(self):
        """Test error handling for invalid inputs"""
        with pytest.raises(ValueError):
            get_action('invalid', 16, 10)
        
        with pytest.raises(ValueError):
            get_action('hard', 4, 10)  # Below minimum
        
        with pytest.raises(ValueError):
            get_action('hard', 22, 10)  # Above maximum
        
        with pytest.raises(ValueError):
            get_action('soft', 12, 10)  # Below minimum
        
        with pytest.raises(ValueError):
            get_action('pair', 1, 10)  # Below minimum
        
        with pytest.raises(ValueError):
            get_action('hard', 16, 1)  # Invalid dealer card

class TestStrategyAdvice:
    """Test the main strategy advice function"""
    
    def test_strategy_advice_format(self):
        """Test that strategy advice returns properly formatted strings"""
        advice = get_strategy_advice(16, 10, 'hard')
        assert "Optimal Basic Strategy action:" in advice
        assert advice.endswith(".")
    
    def test_strategy_advice_actions(self):
        """Test that strategy advice includes correct actions"""
        # Test each action type
        hit_advice = get_strategy_advice(16, 10, 'hard')
        assert "H." in hit_advice
        
        stand_advice = get_strategy_advice(17, 10, 'hard')
        assert "S." in stand_advice
        
        double_advice = get_strategy_advice(11, 6, 'hard')
        assert "D." in double_advice
        
        split_advice = get_strategy_advice(8, 8, 'pair')
        assert "P." in split_advice

class TestActionText:
    """Test action text conversion"""
    
    def test_action_text_conversion(self):
        """Test that action codes convert to readable text"""
        assert get_action_text('H') == 'Hit'
        assert get_action_text('S') == 'Pass'
        assert get_action_text('D') == 'Double'
        assert get_action_text('Ds') == 'Double or Pass'
        assert get_action_text('P') == 'Split'

# Performance test for the strategy table
class TestPerformance:
    """Test that strategy lookups are fast"""
    
    def test_lookup_speed(self):
        """Test that strategy lookups complete quickly"""
        import time
        
        start_time = time.time()
        
        # Perform 1000 lookups
        for _ in range(1000):
            get_action('hard', 16, 10)
        
        end_time = time.time()
        lookup_time = end_time - start_time
        
        # Should complete in well under 1 second
        assert lookup_time < 0.1, f"1000 lookups took {lookup_time:.3f}s (too slow)"

if __name__ == "__main__":
    # Run tests without pytest
    test_strategy = TestStrategyTable()
    test_advice = TestStrategyAdvice() 
    test_text = TestActionText()
    test_perf = TestPerformance()
    
    print("Running comprehensive strategy tests...")
    
    try:
        # Run all test methods
        test_strategy.test_hard_hands_basic_scenarios()
        test_strategy.test_soft_hands_basic_scenarios()
        test_strategy.test_pair_scenarios()
        test_strategy.test_edge_cases()
        test_strategy.test_all_dealer_upcards()
        
        test_advice.test_strategy_advice_format()
        test_advice.test_strategy_advice_actions()
        
        test_text.test_action_text_conversion()
        
        test_perf.test_lookup_speed()
        
        print("✅ All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")