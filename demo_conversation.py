#!/usr/bin/env python3
"""
Demo conversation script to test the bot without interactive input
"""

from hello_bot import HelloBot
import time

def demo_conversation():
    """Simulate a conversation with the bot"""
    print("=== Demo Conversation with Spiritual Discovery Bot ===\n")
    
    bot = HelloBot()
    
    # Sample conversation flow
    conversation = [
        "Hello, I'm interested in discovering my spiritual gifts",
        "I enjoy helping others but I'm not sure what my specific strengths are",
        "I find myself naturally drawn to listening to people's problems",
        "Sometimes I feel overwhelmed by others' emotions though",
        "What kind of spiritual gifts might I have?"
    ]
    
    system_prompt = """You are a wise and encouraging spiritual guide helping people discover their gifts and passions. 
    Respond warmly and ask thoughtful questions that help the person reflect on their strengths, interests, and what brings them joy.
    Keep responses concise but meaningful."""
    
    print("Bot: Hello! I'm your spiritual discovery guide.")
    print("Bot: I'm here to help you explore your gifts and passions.\n")
    
    for i, user_message in enumerate(conversation, 1):
        print(f"User: {user_message}")
        
        # Build the full prompt
        full_prompt = f"{system_prompt}\n\nUser: {user_message}\n\nBot:"
        
        print("Bot: ", end="", flush=True)
        
        # Add a small delay to simulate thinking
        time.sleep(1)
        
        response = bot.call_gemini(full_prompt)
        print(response)
        print("-" * 50)
        
        # Small pause between exchanges
        time.sleep(2)
    
    print("\nDemo conversation complete!")

if __name__ == "__main__":
    try:
        demo_conversation()
    except Exception as e:
        print(f"Error: {e}")