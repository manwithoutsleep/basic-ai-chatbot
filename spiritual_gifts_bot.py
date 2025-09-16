#!/usr/bin/env python3
"""
Phase 3 Complete: Spiritual Gifts Discovery Bot
Integrates all components: question progression, analysis, scoring, and spiritual gifts framework
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

from discovery_engine import DiscoverySession
from analysis_engine import SkillsPassionsAnalyzer
from scoring_system import SpiritualGiftsAssessment

# Load environment variables
load_dotenv()

class SpiritualGiftsDiscoveryBot:
    """Complete spiritual gifts discovery system with all Phase 3 functionality"""

    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}"

        # Initialize all components
        self.discovery_session = DiscoverySession()
        self.analyzer = SkillsPassionsAnalyzer()
        self.assessor = SpiritualGiftsAssessment()

        self.system_prompt = """You are a wise, compassionate spiritual guide specializing in helping people discover their spiritual gifts and life calling.

You have access to structured conversation stages and can provide contextually aware responses that build upon previous insights. Your responses should be:

1. Warm and encouraging
2. Insightful and thought-provoking
3. Connected to previous conversation context
4. Focused on helping the person discover their unique gifts
5. Concise but meaningful

When responding, reference insights from earlier in the conversation and ask follow-up questions that go deeper into their gifts and calling."""

    def call_gemini(self, prompt):
        """Make API call to Gemini with enhanced error handling"""
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
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

            return "I'm having trouble generating a response right now. Could you share more about what you're experiencing?"

        except requests.exceptions.RequestException as e:
            return f"I'm experiencing a connection issue: {str(e)[:100]}..."
        except KeyError as e:
            return f"I'm having trouble processing that. Could you rephrase your response?"

    def start_discovery_journey(self):
        """Begin the complete spiritual gifts discovery experience"""
        print("=" * 80)
        print("SPIRITUAL GIFTS DISCOVERY JOURNEY")
        print("=" * 80)
        print("Welcome to your personalized spiritual gifts discovery experience!")
        print("\nThis journey will guide you through 6 stages:")
        print("  1. Introduction & Connection")
        print("  2. Skills Assessment")
        print("  3. Passion Exploration")
        print("  4. Values Clarification")
        print("  5. Synthesis & Integration")
        print("  6. Recommendations & Next Steps")
        print("\nAt the end, you'll receive a detailed assessment of your spiritual gifts.")
        print("\nCommands: 'quit', 'save', 'progress', 'skip', 'analyze'")
        print("-" * 80)

        # Begin with first question
        first_question = self.discovery_session.get_next_question()
        if first_question:
            print(f"\nGuide: {first_question}")

        while True:
            user_input = input("\nYou: ").strip()

            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                self._handle_session_end()
                break

            elif user_input.lower() == 'save':
                self._save_session()
                continue

            elif user_input.lower() == 'progress':
                self._show_progress()
                continue

            elif user_input.lower() == 'skip':
                self._skip_stage()
                continue

            elif user_input.lower() == 'analyze':
                self._generate_analysis()
                continue

            elif user_input.lower() == 'help':
                self._show_help()
                continue

            if not user_input:
                continue

            # Process the user's response
            success = self.discovery_session.process_response(user_input)
            if not success:
                print("\nGuide: We've completed all discovery stages! Let me generate your spiritual gifts assessment.")
                self._generate_final_assessment()
                break

            # Generate contextual AI response
            current_stage = self.discovery_session.get_current_stage()
            contextual_prompt = self.discovery_session.build_contextual_prompt(current_stage, user_input)

            print("\nGuide: ", end="", flush=True)
            ai_response = self.call_gemini(contextual_prompt)
            print(ai_response)

            # Check if we should provide analysis after certain stages
            if current_stage in ['skills_assessment', 'passion_exploration', 'values_clarification']:
                if self.discovery_session.stage_progress[current_stage].get('completed', False):
                    self._provide_stage_insights(current_stage)

            # Get next question
            next_question = self.discovery_session.get_next_question()
            if next_question:
                print(f"\nNext: {next_question}")
            else:
                current_stage = self.discovery_session.get_current_stage()
                if current_stage == "completed":
                    print("\nDiscovery journey complete! Generating your spiritual gifts assessment...")
                    self._generate_final_assessment()
                    break

    def _handle_session_end(self):
        """Handle when user chooses to quit"""
        filename = self.discovery_session.save_session()
        print(f"\nGuide: Your discovery journey has been saved to {filename}")

        # Offer analysis if enough data collected
        total_responses = sum(len(responses) for responses in self.discovery_session.user_responses.values())
        if total_responses >= 3:
            offer_analysis = input("\nWould you like a partial analysis of what we've discovered so far? (y/n): ")
            if offer_analysis.lower().startswith('y'):
                self._generate_analysis()

        print("\nYour journey of discovery continues beyond our conversation.")
        print("Take time to reflect on what we've explored together.")

    def _save_session(self):
        """Save current session"""
        filename = self.discovery_session.save_session()
        print(f"\nSession saved to {filename}")

    def _show_progress(self):
        """Display current progress"""
        summary = self.discovery_session.get_session_summary()
        current_stage = summary["current_stage"]
        completion = summary["completion_percentage"]

        print(f"\n--- DISCOVERY PROGRESS ---")
        print(f"Current Stage: {current_stage.replace('_', ' ').title()}")
        print(f"Overall Progress: {completion:.1f}%")
        print(f"Total Responses: {summary['total_responses']}")

        # Show stage-by-stage progress
        for stage in self.discovery_session.stages:
            status = "✓" if self.discovery_session.stage_progress[stage]['completed'] else "○"
            count = self.discovery_session.stage_progress[stage]['question_count']
            print(f"  {status} {stage.replace('_', ' ').title()} ({count} responses)")

        print("--- END PROGRESS ---")

    def _skip_stage(self):
        """Skip to next stage"""
        current_stage = self.discovery_session.get_current_stage()
        print(f"\nSkipping {current_stage.replace('_', ' ')} stage...")

        self.discovery_session._advance_to_next_stage()
        next_question = self.discovery_session.get_next_question()

        if next_question:
            new_stage = self.discovery_session.get_current_stage()
            print(f"Moving to {new_stage.replace('_', ' ')} stage.")
            print(f"\nGuide: {next_question}")
        else:
            print("\nGuide: We've completed all discovery stages!")

    def _generate_analysis(self):
        """Generate current analysis of responses"""
        analysis = self.analyzer.generate_analysis_summary(self.discovery_session.user_responses)

        print(f"\n--- CURRENT INSIGHTS ---")
        if analysis['skills_analysis'].get('top_skills'):
            skills = ', '.join(analysis['skills_analysis']['top_skills'])
            print(f"Identified Skills: {skills}")

        if analysis['passions_analysis'].get('top_passions'):
            passions = ', '.join(analysis['passions_analysis']['top_passions'])
            print(f"Core Passions: {passions}")

        if analysis['potential_spiritual_gifts']:
            print(f"\nPotential Gifts Emerging:")
            for gift in analysis['potential_spiritual_gifts'][:3]:
                print(f"  • {gift['name'].title()} ({gift['strength']})")

        print(f"\nAlignment Score: {analysis['alignment_score']}/100")
        print(f"Summary: {analysis['summary']}")
        print("--- END INSIGHTS ---")

    def _provide_stage_insights(self, completed_stage):
        """Provide insights after completing a major stage"""
        responses = self.discovery_session.user_responses.get(completed_stage, [])
        if not responses:
            return

        stage_names = {
            'skills_assessment': 'Skills',
            'passion_exploration': 'Passions',
            'values_clarification': 'Values'
        }

        stage_name = stage_names.get(completed_stage, completed_stage)
        print(f"\n{stage_name} Stage Complete - Quick Insight:")

        if completed_stage == 'skills_assessment':
            skills_analysis = self.analyzer.analyze_skills(responses)
            if skills_analysis.get('top_skills'):
                skills_text = ', '.join(skills_analysis['top_skills'])
                print(f"Your strongest skills appear to center around: {skills_text}")

        elif completed_stage == 'passion_exploration':
            passions_analysis = self.analyzer.analyze_passions(responses)
            if passions_analysis.get('top_passions'):
                passions_text = ', '.join(passions_analysis['top_passions'])
                print(f"Your core passions seem to involve: {passions_text}")

        elif completed_stage == 'values_clarification':
            print("Your values are becoming clearer - this will help us see how your gifts might be expressed.")

    def _generate_final_assessment(self):
        """Generate and display the complete spiritual gifts assessment"""
        print("\n" + "=" * 60)
        print("SPIRITUAL GIFTS ASSESSMENT RESULTS")
        print("=" * 60)

        assessment = self.assessor.generate_comprehensive_assessment(self.discovery_session.user_responses)

        # Display top gifts
        print(f"\nREADINESS SCORE: {assessment['readiness_score']}/100")
        print(f"\nYOUR TOP SPIRITUAL GIFTS:")

        for i, gift in enumerate(assessment['top_gifts'], 1):
            print(f"\n{i}. {gift['name'].upper()} - {gift['score']}% ({gift['strength']})")
            print(f"   {gift['description']}")

        # Show dominant gifts separately if any
        if assessment['dominant_gifts']:
            print(f"\nDOMINANT GIFTS (Strongest Indicators):")
            for gift in assessment['dominant_gifts']:
                print(f"   • {gift['name'].title()} ({gift['score']}%)")

        # Display recommendations
        print(f"\nPERSONALIZED RECOMMENDATIONS:")
        for i, rec in enumerate(assessment['recommendations'], 1):
            print(f"{i}. {rec}")

        # Display next steps
        print(f"\nSUGGESTED NEXT STEPS:")
        for i, step in enumerate(assessment['next_steps'], 1):
            print(f"{i}. {step}")

        # Save assessment
        filename = self.assessor.save_assessment(assessment)
        session_filename = self.discovery_session.save_session()

        print(f"\nSAVED FILES:")
        print(f"   Assessment: {filename}")
        print(f"   Session: {session_filename}")

        print(f"\n" + "=" * 60)
        print("Your spiritual gifts discovery journey is complete!")
        print("May you step boldly into using these gifts to serve others.")
        print("=" * 60)

    def _show_help(self):
        """Display help information"""
        print(f"\n--- HELP ---")
        print("Commands you can use anytime:")
        print("  'quit' - End session and save")
        print("  'save' - Save current progress")
        print("  'progress' - View current progress")
        print("  'skip' - Skip to next stage")
        print("  'analyze' - Get current insights")
        print("  'help' - Show this help")
        print("\nJust type your responses naturally to continue the discovery process.")
        print("--- END HELP ---")


if __name__ == "__main__":
    try:
        bot = SpiritualGiftsDiscoveryBot()
        bot.start_discovery_journey()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please make sure you have GOOGLE_API_KEY set in your .env file")
    except KeyboardInterrupt:
        print("\n\nGoodbye! Your journey continues...")