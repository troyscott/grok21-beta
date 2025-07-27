from blackjack_game import get_strategy_advice

# Test with valid inputs
print("Valid inputs:")
print(f"Hard 12 vs 10: {get_strategy_advice(12, 10, 'hard')}")
print(f"Soft 18 vs 6: {get_strategy_advice(18, 6, 'soft')}")
print(f"Pair 8 vs 7: {get_strategy_advice(8, 7, 'pair')}")

# Test with edge cases
print("\nEdge cases:")
print(f"Hard 5 vs 2: {get_strategy_advice(5, 2, 'hard')}")
print(f"Hard 21 vs 11: {get_strategy_advice(21, 11, 'hard')}")
print(f"Soft 13 vs 2: {get_strategy_advice(13, 2, 'soft')}")
print(f"Soft 20 vs 10: {get_strategy_advice(20, 10, 'soft')}")
print(f"Pair 2 vs 2: {get_strategy_advice(2, 2, 'pair')}")
print(f"Pair 11 vs 11: {get_strategy_advice(11, 11, 'pair')}")

# Test with invalid inputs
print("\nInvalid inputs:")
print(f"Invalid hand type: {get_strategy_advice(12, 10, 'invalid')}")
print(f"Invalid player value (hard): {get_strategy_advice(4, 10, 'hard')}")
print(f"Invalid player value (soft): {get_strategy_advice(12, 10, 'soft')}")
print(f"Invalid player value (pair): {get_strategy_advice(12, 10, 'pair')}")
print(f"Invalid dealer upcard: {get_strategy_advice(12, 1, 'hard')}")
print(f"Invalid dealer upcard: {get_strategy_advice(12, 12, 'hard')}")

# Test with non-integer inputs
print("\nNon-integer inputs:")
print(f"Non-integer player value: {get_strategy_advice('12', 10, 'hard')}")
print(f"Non-integer dealer upcard: {get_strategy_advice(12, '10', 'hard')}")