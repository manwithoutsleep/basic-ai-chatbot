#!/usr/bin/env python3
"""
Basic AI Chatbot - Hello World Version
Phase 1: Simple API integration with Google Gemini
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class HelloBot:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Gemini API endpoint
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}"
        
    def call_gemini(self, prompt):
        """Make a request to Google Gemini API"""
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(self.api_url, 
                                   headers=headers, 
                                   data=json.dumps(payload))
            response.raise_for_status()
            
            data = response.json()
            
            # Extract the generated text from the response
            if 'candidates' in data and len(data['candidates']) > 0:
                if 'content' in data['candidates'][0]:
                    parts = data['candidates'][0]['content']['parts']
                    if len(parts) > 0 and 'text' in parts[0]:
                        return parts[0]['text']
            
            return "Sorry, I couldn't generate a response."
            
        except requests.exceptions.RequestException as e:
            return f"Error calling API: {e}"
        except KeyError as e:
            return f"Error parsing response: {e}"
    
    def chat(self):
        """Simple chat loop"""
        print("Hello! I'm your spiritual discovery guide.")
        print("I'm here to help you explore your gifts and passions.")
        print("Type 'quit' to exit.\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Bot: Thank you for chatting! May your journey of self-discovery continue to flourish.")
                break
            
            if not user_input:
                continue
                
            # Create a spiritual discovery focused prompt
            system_prompt = """You are a wise and encouraging spiritual guide helping people discover their gifts and passions. 
            Respond warmly and ask thoughtful questions that help the person reflect on their strengths, interests, and what brings them joy.
            Keep responses concise but meaningful."""
            
            full_prompt = f"{system_prompt}\n\nUser: {user_input}\n\nBot:"
            
            print("Bot: ", end="")
            response = self.call_gemini(full_prompt)
            print(response)
            print()

if __name__ == "__main__":
    try:
        bot = HelloBot()
        bot.chat()
    except ValueError as e:
        print(f"Configuration error: {e}")
    except KeyboardInterrupt:
        print("\nGoodbye!")