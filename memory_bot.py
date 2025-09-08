#!/usr/bin/env python3
"""
Phase 2: Conversation Management Bot
Adds memory and multi-turn conversation capabilities
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ConversationMemory:
    """Manages conversation history and context"""
    
    def __init__(self):
        self.messages = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.max_history = 10  # Keep last 10 exchanges to manage token limits
        
    def add_message(self, role, content):
        """Add a message to conversation history"""
        self.messages.append({
            "role": role,  # "user" or "bot"
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only recent messages to avoid token limits
        if len(self.messages) > self.max_history * 2:  # 2 messages per exchange
            self.messages = self.messages[-self.max_history * 2:]
    
    def get_context(self):
        """Build conversation context for API call"""
        context = ""
        for msg in self.messages:
            if msg["role"] == "user":
                context += f"User: {msg['content']}\n"
            else:
                context += f"Bot: {msg['content']}\n"
        return context.strip()
    
    def save_session(self, filename=None):
        """Save conversation to JSON file"""
        if not filename:
            filename = f"sessions/session_{self.session_id}.json"
        
        # Create sessions directory if it doesn't exist
        os.makedirs("sessions", exist_ok=True)
        
        session_data = {
            "session_id": self.session_id,
            "created": self.messages[0]["timestamp"] if self.messages else datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "message_count": len(self.messages),
            "messages": self.messages
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        return filename

class MemoryBot:
    """Enhanced bot with conversation memory"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}"
        self.memory = ConversationMemory()
        
        # System prompt for spiritual discovery
        self.system_prompt = """You are a wise and encouraging spiritual guide helping people discover their gifts and passions. 
        You have memory of our previous conversation. Reference earlier topics naturally when relevant.
        Ask thoughtful follow-up questions based on what the person has already shared.
        Help them explore the connection between their skills (what they're good at) and their passions (what they enjoy).
        Keep responses warm, insightful, and concise."""
    
    def call_gemini(self, user_input):
        """Make API call with conversation context"""
        
        # Build full prompt with conversation history
        context = self.memory.get_context()
        if context:
            full_prompt = f"{self.system_prompt}\n\nPrevious conversation:\n{context}\n\nUser: {user_input}\n\nBot:"
        else:
            full_prompt = f"{self.system_prompt}\n\nUser: {user_input}\n\nBot:"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": full_prompt
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
        """Enhanced chat with memory"""
        print("=" * 60)
        print("🌟 Spiritual Discovery Bot - Now with Memory! 🌟")
        print("=" * 60)
        print("Hello! I'm your spiritual discovery guide.")
        print("I'll remember our conversation as we explore your gifts and passions together.")
        print("Type 'quit' to exit, 'save' to save our session, or 'history' to see our conversation.")
        print("-" * 60)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                # Save session on exit
                filename = self.memory.save_session()
                print(f"\nBot: Thank you for our meaningful conversation! Your session has been saved to {filename}")
                print("May your journey of self-discovery continue to flourish. 🙏")
                break
            
            if user_input.lower() == 'save':
                filename = self.memory.save_session()
                print(f"\nSession saved to {filename}")
                continue
                
            if user_input.lower() == 'history':
                print("\n--- Conversation History ---")
                for msg in self.memory.messages:
                    role_icon = "👤" if msg["role"] == "user" else "🤖"
                    print(f"{role_icon} {msg['role'].title()}: {msg['content']}")
                print("--- End History ---")
                continue
            
            if not user_input:
                continue
            
            # Add user message to memory
            self.memory.add_message("user", user_input)
            
            print("\nBot: ", end="", flush=True)
            response = self.call_gemini(user_input)
            print(response)
            
            # Add bot response to memory
            self.memory.add_message("bot", response)

if __name__ == "__main__":
    try:
        bot = MemoryBot()
        bot.chat()
    except ValueError as e:
        print(f"Configuration error: {e}")
    except KeyboardInterrupt:
        print("\nGoodbye!")