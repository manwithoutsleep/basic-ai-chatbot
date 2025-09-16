#!/usr/bin/env python3
"""
Phase 4 Complete: Enhanced Intelligence Discovery Bot
Integrates context-awareness, dynamic questioning, and personality profiling

Key Architecture Integration:
1. Context-Aware Responses: References previous insights naturally
2. Dynamic Questioning: Adapts questions based on emerging patterns
3. Personality Profiling: Matches communication style to user preferences
4. Intelligent Orchestration: Coordinates all systems for coherent experience
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Import Phase 4 components
from context_manager import EnhancedContextManager
from dynamic_questioning import DynamicQuestioningEngine
from personality_profiler import PersonalityProfiler

# Import Phase 3 components for compatibility
from discovery_engine import DiscoverySession
from scoring_system import SpiritualGiftsAssessment

# Load environment variables
load_dotenv()

class EnhancedSpiritualDiscoveryBot:
    """
    Advanced AI chatbot with enhanced intelligence capabilities

    Architecture Overview:
    - Context Manager: Maintains conversation awareness
    - Dynamic Questioning: Adapts flow based on patterns
    - Personality Profiler: Matches communication style
    - Intelligence Orchestrator: Coordinates all systems
    """

    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}"

        # Initialize all intelligence systems
        self.context_manager = EnhancedContextManager()
        self.dynamic_questioner = DynamicQuestioningEngine()
        self.personality_profiler = PersonalityProfiler()

        # Compatibility with Phase 3 systems
        self.discovery_session = DiscoverySession()
        self.assessor = SpiritualGiftsAssessment()

        # Enhanced system state
        self.conversation_stage = "introduction"
        self.session_start_time = datetime.now()
        self.total_exchanges = 0

    def call_gemini_with_intelligence(self, user_input: str) -> str:
        """
        Enhanced LLM call with intelligent context and style adaptation

        Architecture Concept: Intelligent Prompt Engineering
        - Injects relevant context automatically
        - Provides style guidance based on user personality
        - Includes dynamic questioning suggestions
        """

        # Build intelligent context
        context = self.context_manager.build_context_for_llm(user_input)

        # Get style guidance
        style_guidance = self.personality_profiler.get_style_guidance_for_llm()

        # Get contextual stage guidance
        contextual_guidance = self.context_manager.get_contextual_guidance(self.conversation_stage)

        # Build enhanced prompt
        enhanced_prompt = f"""You are a wise, compassionate spiritual guide helping someone discover their gifts and calling.

{style_guidance}

{contextual_guidance}

CONVERSATION CONTEXT:
{context}

Respond naturally while following the style guidance. Reference previous insights when relevant. Ask thoughtful follow-up questions that build on what you've learned about them.

Your response:"""

        # Make API call
        payload = {
            "contents": [{
                "parts": [{
                    "text": enhanced_prompt
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

            return "I'm having trouble generating a response. Could you share more about what you're experiencing?"

        except requests.exceptions.RequestException as e:
            return f"I'm experiencing a connection issue. Let's continue - could you tell me more?"
        except KeyError as e:
            return f"I'm having trouble processing that. Could you rephrase your response?"

    def get_next_intelligent_question(self, user_input: str) -> str:
        """
        Generate next question using dynamic questioning intelligence

        Architecture Concept: Adaptive Conversation Flow
        """

        # Generate dynamic question
        dynamic_question = self.dynamic_questioner.generate_next_question(
            self.discovery_session.user_responses,
            self.conversation_stage,
            user_input
        )

        # Check if we should suggest deep dive
        strong_themes = [name for name, theme in self.context_manager.themes.items() if theme.strength >= 2.5]

        if strong_themes and dynamic_question.question_type.value == "deep_dive":
            return f"\n{dynamic_question.question_text}"
        elif dynamic_question.question_type.value == "follow_up":
            return f"\n{dynamic_question.question_text}"
        elif self._should_continue_dynamic_flow():
            return f"\n{dynamic_question.question_text}"
        else:
            # Fall back to standard progression if appropriate
            return ""

    def _should_continue_dynamic_flow(self) -> bool:
        """Determine if we should continue with dynamic flow or standard progression"""

        # Continue dynamic flow if we have strong patterns
        strong_patterns = len([p for p in self.dynamic_questioner.response_patterns if p.confidence >= 0.8])

        # Or if we haven't covered minimum areas
        uncovered_areas = [area for area, covered in self.dynamic_questioner.coverage_status.items() if not covered]

        return strong_patterns > 0 or len(uncovered_areas) > 2

    def start_enhanced_discovery_journey(self):
        """
        Begin the enhanced discovery experience with all intelligence systems active
        """
        print("=" * 80)
        print("ENHANCED SPIRITUAL GIFTS DISCOVERY JOURNEY")
        print("=" * 80)
        print("Welcome to an intelligent, personalized spiritual gifts discovery experience!")
        print("\nThis enhanced system will:")
        print("  • Remember and reference your previous insights")
        print("  • Adapt questions based on patterns in your responses")
        print("  • Match my communication style to your preferences")
        print("  • Provide a truly personalized discovery journey")
        print("\nCommands: 'quit', 'save', 'progress', 'insights', 'style'")
        print("-" * 80)

        # Start with first question
        first_question = self.discovery_session.get_next_question()
        if first_question:
            print(f"\nGuide: {first_question}")

        while True:
            user_input = input("\nYou: ").strip()

            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                self._handle_enhanced_session_end()
                break

            elif user_input.lower() == 'save':
                self._save_enhanced_session()
                continue

            elif user_input.lower() == 'progress':
                self._show_enhanced_progress()
                continue

            elif user_input.lower() == 'insights':
                self._show_current_insights()
                continue

            elif user_input.lower() == 'style':
                self._show_personality_profile()
                continue

            elif user_input.lower() == 'help':
                self._show_enhanced_help()
                continue

            if not user_input:
                continue

            # Process with all intelligence systems
            self._process_user_input_with_intelligence(user_input)

            # Generate intelligent response
            print("\nGuide: ", end="", flush=True)
            ai_response = self.call_gemini_with_intelligence(user_input)
            print(ai_response)

            # Record the exchange
            self.context_manager.add_exchange(user_input, ai_response, self.conversation_stage)
            self.total_exchanges += 1

            # Get next question intelligently
            next_question = self.get_next_intelligent_question(user_input)
            if next_question:
                print(next_question)

            # Check if we should advance stage or continue with intelligence
            if self._should_advance_stage():
                self._advance_conversation_stage()

    def _process_user_input_with_intelligence(self, user_input: str):
        """Process user input through all intelligence systems"""

        # Update discovery session
        self.discovery_session.process_response(user_input)

        # Update personality profile
        self.personality_profiler.update_profile(user_input)

        # Update conversation stage
        self.conversation_stage = self.discovery_session.get_current_stage()

    def _should_advance_stage(self) -> bool:
        """Intelligent stage advancement decision"""

        current_stage = self.discovery_session.get_current_stage()
        stage_responses = len(self.discovery_session.user_responses.get(current_stage, []))

        # Use dynamic questioning logic
        return not self.dynamic_questioner.should_continue_current_stage(current_stage, stage_responses)

    def _advance_conversation_stage(self):
        """Advance to next stage with intelligence"""

        # Advance discovery session
        self.discovery_session._advance_to_next_stage()
        self.conversation_stage = self.discovery_session.get_current_stage()

        # Provide stage transition insight
        if self.conversation_stage != "completed":
            print(f"\n--- Moving to {self.conversation_stage.replace('_', ' ').title()} Stage ---")

            # Provide intelligent transition based on context
            strong_themes = [name for name, theme in self.context_manager.themes.items() if theme.strength >= 2.0]
            if strong_themes:
                print(f"I'm noticing strong themes around {', '.join(strong_themes[:2])} - let's explore this further.")

    def _handle_enhanced_session_end(self):
        """Handle session end with intelligence summary"""

        print(f"\nThank you for this meaningful discovery journey!")

        # Provide intelligent summary
        insights_summary = self.context_manager.get_conversation_summary()
        personality_summary = self.personality_profiler.get_profile_summary()

        print(f"\nSession Summary:")
        print(f"  • Total exchanges: {insights_summary['total_exchanges']}")
        print(f"  • Insights discovered: {insights_summary['high_confidence_insights']}")
        print(f"  • Themes identified: {len(insights_summary['themes'])}")

        if personality_summary.get('primary_style'):
            print(f"  • Communication style: {personality_summary['primary_style']}")

        # Save session
        session_filename = self.discovery_session.save_session()
        context_filename = f"context_{self.discovery_session.session_id}.json"
        self.context_manager.save_context(context_filename)

        print(f"\nSaved: {session_filename}, {context_filename}")
        print("Your journey of discovery continues!")

    def _save_enhanced_session(self):
        """Save all enhanced session data"""

        session_filename = self.discovery_session.save_session()
        context_filename = f"context_{self.discovery_session.session_id}.json"
        self.context_manager.save_context(context_filename)

        print(f"\nEnhanced session saved:")
        print(f"  • Discovery data: {session_filename}")
        print(f"  • Context data: {context_filename}")

    def _show_enhanced_progress(self):
        """Show progress with intelligence insights"""

        # Standard progress
        summary = self.discovery_session.get_session_summary()
        print(f"\n--- ENHANCED PROGRESS ---")
        print(f"Current Stage: {summary['current_stage'].replace('_', ' ').title()}")
        print(f"Overall Progress: {summary['completion_percentage']:.1f}%")
        print(f"Total Exchanges: {self.total_exchanges}")

        # Intelligence insights
        context_summary = self.context_manager.get_conversation_summary()
        print(f"High-Confidence Insights: {context_summary['high_confidence_insights']}")

        # Show top themes
        if self.context_manager.themes:
            top_themes = sorted(self.context_manager.themes.items(), key=lambda x: x[1].strength, reverse=True)[:3]
            print(f"Emerging Themes:")
            for theme_name, theme in top_themes:
                print(f"  • {theme_name.title()}: {theme.strength:.1f} strength")

        print("--- END PROGRESS ---")

    def _show_current_insights(self):
        """Show current insights discovered"""

        print(f"\n--- CURRENT INSIGHTS ---")

        if self.context_manager.insights:
            recent_insights = self.context_manager.insights[-3:]  # Last 3 insights
            for insight in recent_insights:
                print(f"• {insight.stage}: {insight.content[:100]}... (confidence: {insight.confidence:.2f})")
        else:
            print("No high-confidence insights discovered yet.")

        print("--- END INSIGHTS ---")

    def _show_personality_profile(self):
        """Show current personality profile"""

        profile_summary = self.personality_profiler.get_profile_summary()

        print(f"\n--- PERSONALITY PROFILE ---")

        if profile_summary.get('primary_style'):
            print(f"Communication Style: {profile_summary['primary_style'].title()}")
            print(f"Preferred Depth: {profile_summary['preferred_depth'].title()}")
            print(f"Confidence: {profile_summary['confidence']:.2f}")
            print(f"Based on {profile_summary['total_samples']} communication samples")
        else:
            print("Building personality profile... need more responses.")

        print("--- END PROFILE ---")

    def _show_enhanced_help(self):
        """Show enhanced help information"""

        print(f"\n--- ENHANCED HELP ---")
        print("Commands:")
        print("  'quit' - End session with intelligent summary")
        print("  'save' - Save enhanced session data")
        print("  'progress' - View progress with intelligence insights")
        print("  'insights' - Show discovered insights")
        print("  'style' - Show your communication style profile")
        print("  'help' - Show this help")
        print("\nThe enhanced system adapts to your communication style and")
        print("remembers insights throughout our conversation.")
        print("--- END HELP ---")


if __name__ == "__main__":
    try:
        bot = EnhancedSpiritualDiscoveryBot()
        bot.start_enhanced_discovery_journey()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please make sure you have GOOGLE_API_KEY set in your .env file")
    except KeyboardInterrupt:
        print("\n\nYour enhanced discovery journey continues...")