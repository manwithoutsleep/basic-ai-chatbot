#!/usr/bin/env python3
"""
Phase 2 Enhanced: Smart Memory Bot with Conversation Summarization
Maintains long-term context through intelligent summarization
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SmartConversationMemory:
    """Enhanced memory with conversation summarization"""
    
    def __init__(self):
        self.messages = []
        self.conversation_summary = ""  # Summary of older conversation parts
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.recent_message_limit = 6  # Keep last 6 messages in full detail
        self.summarize_threshold = 10   # Summarize when we hit 10 messages
        
    def add_message(self, role, content):
        """Add a message to conversation history"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Check if we need to summarize old messages
        if len(self.messages) >= self.summarize_threshold:
            self._summarize_old_messages()
    
    def _summarize_old_messages(self):
        """Summarize older messages and keep recent ones"""
        # Messages to summarize (all but the most recent)
        messages_to_summarize = self.messages[:-self.recent_message_limit]
        recent_messages = self.messages[-self.recent_message_limit:]
        
        if not messages_to_summarize:
            return
            
        # Build text of old messages for summarization
        old_conversation = ""
        for msg in messages_to_summarize:
            role = msg["role"].title()
            old_conversation += f"{role}: {msg['content']}\n"
        
        # Create summarization prompt
        summary_prompt = f"""Please create a concise summary of this conversation between a user and a spiritual discovery guide. Focus on:
1. Key insights about the user's gifts, skills, and passions
2. Important personal details shared
3. Main themes and discoveries
4. Any specific interests or challenges mentioned

Previous summary (if any): {self.conversation_summary}

Conversation to summarize:
{old_conversation}

Provide a clear, comprehensive summary that preserves the essential context for future conversation:"""
        
        # Get summary from API (we'll need the API instance for this)
        # For now, create a basic summary structure
        user_details = []
        key_themes = []
        
        for msg in messages_to_summarize:
            if msg["role"] == "user":
                # Extract key information from user messages
                content = msg["content"].lower()
                if "name" in content or "i'm" in content or "my name" in content:
                    user_details.append(msg["content"])
                if any(word in content for word in ["love", "enjoy", "passionate", "interested", "drawn to"]):
                    key_themes.append(msg["content"])
        
        # Create structured summary
        summary_parts = []
        if self.conversation_summary:
            summary_parts.append(f"Previous context: {self.conversation_summary}")
        if user_details:
            summary_parts.append(f"User shared: {'; '.join(user_details[:3])}")
        if key_themes:
            summary_parts.append(f"Key interests: {'; '.join(key_themes[:3])}")
        
        # Update summary and keep only recent messages
        self.conversation_summary = " | ".join(summary_parts)
        self.messages = recent_messages
        
        print(f"\n[System: Summarized {len(messages_to_summarize)} older messages to preserve context]\n")
    
    def get_context(self):
        """Build conversation context with summary and recent messages"""
        context_parts = []
        
        # Add conversation summary if available
        if self.conversation_summary:
            context_parts.append(f"CONVERSATION SUMMARY: {self.conversation_summary}")
            context_parts.append("")  # Blank line separator
        
        # Add recent messages in full detail
        context_parts.append("RECENT CONVERSATION:")
        for msg in self.messages:
            role = msg["role"].title()
            context_parts.append(f"{role}: {msg['content']}")
        
        return "\n".join(context_parts)
    
    def get_summary_with_api(self, api_call_function):
        """Enhanced summarization using the actual API"""
        if len(self.messages) < self.summarize_threshold:
            return
            
        messages_to_summarize = self.messages[:-self.recent_message_limit]
        recent_messages = self.messages[-self.recent_message_limit:]
        
        # Build conversation text
        old_conversation = ""
        for msg in messages_to_summarize:
            role = msg["role"].title()
            old_conversation += f"{role}: {msg['content']}\n"
        
        # Create summarization prompt
        summary_prompt = f"""Please create a concise summary of this spiritual discovery conversation. Focus on:
- Key insights about the user's gifts, skills, and passions
- Important personal details (name, interests, challenges)
- Main themes and discoveries so far

Previous summary: {self.conversation_summary or "None"}

Conversation to summarize:
{old_conversation}

Summary (2-3 sentences max):"""
        
        try:
            # Use the API to create a better summary
            new_summary = api_call_function(summary_prompt)
            self.conversation_summary = new_summary
            self.messages = recent_messages
            print(f"\n[System: Intelligently summarized conversation - {len(messages_to_summarize)} messages condensed]\n")
        except Exception as e:
            print(f"\n[System: Summary failed, using basic approach: {e}]\n")
            self._summarize_old_messages()  # Fallback to basic summary
    
    def save_session(self, filename=None):
        """Save conversation with summary to JSON file"""
        if not filename:
            filename = f"sessions/session_{self.session_id}.json"
        
        os.makedirs("sessions", exist_ok=True)
        
        session_data = {
            "session_id": self.session_id,
            "created": self.messages[0]["timestamp"] if self.messages else datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "conversation_summary": self.conversation_summary,
            "recent_message_count": len(self.messages),
            "messages": self.messages
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        return filename

class SmartMemoryBot:
    """Enhanced bot with intelligent conversation summarization"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}"
        self.memory = SmartConversationMemory()
        
        self.system_prompt = """You are a wise and encouraging spiritual guide helping people discover their gifts and passions. 
        You have access to a conversation summary and recent detailed messages. Use both to provide contextually aware responses.
        Reference previous insights naturally and build upon earlier discoveries.
        Ask thoughtful follow-up questions that help explore the connection between skills and passions.
        Keep responses warm, insightful, and concise."""
    
    def call_gemini(self, user_input):
        """Make API call with smart context management"""
        context = self.memory.get_context()
        full_prompt = f"{self.system_prompt}\n\n{context}\n\nUser: {user_input}\n\nBot:"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": full_prompt
                }]
            }]
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
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
    
    def _api_call_for_summary(self, prompt):
        """Helper method for summarization API calls"""
        return self.call_gemini(prompt)
    
    def chat(self):
        """Enhanced chat with smart memory management"""
        print("=" * 70)
        print("🧠 Smart Memory Spiritual Discovery Bot 🌟")
        print("=" * 70)
        print("Hello! I'm your spiritual discovery guide with enhanced memory.")
        print("I'll intelligently summarize our conversation to maintain long-term context.")
        print("Commands: 'quit', 'save', 'history', 'summary'")
        print("-" * 70)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                filename = self.memory.save_session()
                print(f"\nBot: Our journey together has been meaningful! Session saved to {filename}")
                print("May your path of discovery continue to unfold beautifully. 🙏")
                break
            
            if user_input.lower() == 'save':
                filename = self.memory.save_session()
                print(f"\nSession saved to {filename}")
                continue
                
            if user_input.lower() == 'summary':
                if self.memory.conversation_summary:
                    print(f"\n--- Conversation Summary ---")
                    print(self.memory.conversation_summary)
                    print("--- End Summary ---")
                else:
                    print("\nNo conversation summary available yet.")
                continue
                
            if user_input.lower() == 'history':
                print(f"\n--- Recent Conversation ({len(self.memory.messages)} messages) ---")
                for msg in self.memory.messages:
                    role_icon = "👤" if msg["role"] == "user" else "🤖"
                    print(f"{role_icon} {msg['role'].title()}: {msg['content']}")
                if self.memory.conversation_summary:
                    print(f"\n📋 Summary of earlier conversation: {self.memory.conversation_summary}")
                print("--- End History ---")
                continue
            
            if not user_input:
                continue
            
            # Add user message and potentially trigger summarization
            self.memory.add_message("user", user_input)
            
            # Check if we should do intelligent summarization
            if len(self.memory.messages) >= self.memory.summarize_threshold:
                self.memory.get_summary_with_api(self._api_call_for_summary)
            
            print("\nBot: ", end="", flush=True)
            response = self.call_gemini(user_input)
            print(response)
            
            self.memory.add_message("bot", response)

if __name__ == "__main__":
    try:
        bot = SmartMemoryBot()
        bot.chat()
    except ValueError as e:
        print(f"Configuration error: {e}")
    except KeyboardInterrupt:
        print("\nGoodbye!")