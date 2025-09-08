#!/usr/bin/env python3
"""
Test smart memory bot with conversation summarization
"""

from smart_memory_bot import SmartMemoryBot
import time

def test_long_conversation():
    """Test conversation that exceeds message limit to trigger summarization"""
    print("=== Testing Smart Memory with Summarization ===\n")
    
    bot = SmartMemoryBot()
    
    # Extended conversation that will trigger summarization
    long_conversation = [
        "Hi, I'm Alex and I'm 28 years old",
        "I work as a software engineer but I'm not sure it's my calling",
        "I've always been drawn to helping people with their problems",
        "In my free time, I volunteer at a local community center",
        "I really enjoy mentoring younger developers at work",
        "People often come to me for advice about career decisions",
        "I'm good at breaking down complex problems into simple steps",
        "Sometimes I wonder if I should become a counselor or coach",
        "I also love creative writing and have published a few articles",
        "What patterns do you see in what I've shared?",
        "How do my technical skills connect with my people-helping interests?",
        "What specific next steps would you recommend for exploring this?"
    ]
    
    print(f"Starting conversation with {len(long_conversation)} exchanges...")
    print("This will trigger summarization after 10 messages.\n")
    
    for i, user_msg in enumerate(long_conversation, 1):
        print(f"--- Message {i} ---")
        print(f"You: {user_msg}")
        
        # Add user message (this might trigger summarization)
        bot.memory.add_message("user", user_msg)
        
        # Trigger summarization if needed
        if len(bot.memory.messages) >= bot.memory.summarize_threshold:
            print("\n🧠 [Triggering intelligent summarization...]\n")
            bot.memory.get_summary_with_api(bot._api_call_for_summary)
        
        # Get bot response
        response = bot.call_gemini(user_msg)
        bot.memory.add_message("bot", response)
        
        print(f"Bot: {response}")
        print()
        
        # Show memory status
        if i % 5 == 0:  # Every 5 messages
            print(f"Memory Status:")
            print(f"   Recent messages: {len(bot.memory.messages)}")
            if bot.memory.conversation_summary:
                print(f"   Summary: {bot.memory.conversation_summary[:100]}...")
            print()
        
        time.sleep(0.5)  # Small delay
    
    # Final memory state
    print("=" * 60)
    print("FINAL MEMORY STATE:")
    print("=" * 60)
    print(f"Recent messages in memory: {len(bot.memory.messages)}")
    print(f"\nConversation summary:")
    print(bot.memory.conversation_summary)
    print(f"\nRecent conversation context:")
    print("-" * 40)
    context = bot.memory.get_context()
    print(context)
    
    # Save session
    filename = bot.memory.save_session("test_smart_memory_session.json")
    print(f"\nTest session saved to: {filename}")

if __name__ == "__main__":
    try:
        test_long_conversation()
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()