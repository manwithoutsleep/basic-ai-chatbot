#!/usr/bin/env python3
"""
Test script for memory bot functionality
"""

from memory_bot import MemoryBot
import time

def test_memory_conversation():
    """Test that the bot remembers previous context"""
    print("=== Testing Memory Bot Conversation ===\n")
    
    bot = MemoryBot()
    
    # Simulate a conversation that tests memory
    test_exchanges = [
        ("Hello, my name is Sarah and I love helping people", "initial_introduction"),
        ("I'm particularly drawn to listening to others", "specific_interest"),
        ("What did I say my name was?", "memory_test_name"),
        ("And what did I say I love doing?", "memory_test_activity"),
        ("Based on what I've shared, what gifts might I have?", "synthesis_question")
    ]
    
    print("Starting conversation to test memory...\n")
    
    for i, (user_msg, test_label) in enumerate(test_exchanges, 1):
        print(f"--- Exchange {i}: {test_label} ---")
        print(f"User: {user_msg}")
        
        # Add to memory and get response
        bot.memory.add_message("user", user_msg)
        response = bot.call_gemini(user_msg)
        bot.memory.add_message("bot", response)
        
        print(f"Bot: {response}")
        print()
        
        time.sleep(1)  # Small delay between exchanges
    
    # Show final conversation context
    print("--- Final Conversation Context ---")
    context = bot.memory.get_context()
    print(context)
    print()
    
    # Save the test session
    filename = bot.memory.save_session("test_memory_session.json")
    print(f"Test session saved to: {filename}")

if __name__ == "__main__":
    try:
        test_memory_conversation()
    except Exception as e:
        print(f"Test failed: {e}")