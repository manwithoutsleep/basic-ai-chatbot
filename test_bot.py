#!/usr/bin/env python3
"""
Test script for the basic AI chatbot API connection
"""

from hello_bot import HelloBot

def test_api_connection():
    """Test that we can successfully call the Gemini API"""
    print("Testing Gemini API connection...")
    
    try:
        bot = HelloBot()
        
        # Test with a simple prompt
        test_prompt = "Hello! Can you introduce yourself as a spiritual discovery guide in one sentence?"
        
        print(f"Sending test prompt: {test_prompt}")
        response = bot.call_gemini(test_prompt)
        
        print(f"API Response: {response}")
        
        if "Error" in response:
            print("Test failed - API returned an error")
            return False
        else:
            print("Test passed - API is working!")
            return True
            
    except Exception as e:
        print(f"Test failed with exception: {e}")
        return False

if __name__ == "__main__":
    test_api_connection()