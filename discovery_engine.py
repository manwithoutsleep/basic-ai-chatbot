#!/usr/bin/env python3
"""
Phase 3: Self-Discovery Logic Engine
Implements structured question progression system for spiritual gifts discovery
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DiscoverySession:
    """Manages the structured self-discovery journey with progressive stages"""

    def __init__(self):
        self.stages = [
            "introduction",
            "skills_assessment",
            "passion_exploration",
            "values_clarification",
            "synthesis",
            "recommendations"
        ]

        self.current_stage = 0
        self.stage_progress = {}  # Track progress within each stage
        self.user_responses = {}  # Store responses by category
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Initialize response storage
        for stage in self.stages:
            self.user_responses[stage] = []
            self.stage_progress[stage] = {"completed": False, "question_count": 0}

    def get_current_stage(self):
        """Get current stage name"""
        if self.current_stage < len(self.stages):
            return self.stages[self.current_stage]
        return "completed"

    def get_stage_questions(self, stage):
        """Get question templates for each stage"""
        question_templates = {
            "introduction": [
                "Hello! I'm excited to guide you on this journey of self-discovery. What's your name, and what drew you to explore your spiritual gifts and passions today?",
                "Tell me a bit about yourself - what brings you joy in your daily life?",
                "Have you ever taken any personality or spiritual gifts assessments before? What did you learn?"
            ],

            "skills_assessment": [
                "Let's explore your natural talents. What activities do you find yourself excelling at with minimal effort?",
                "Think about compliments you often receive from others. What strengths do people frequently notice in you?",
                "What skills have you developed over the years that others come to you for help with?",
                "In what areas do you feel confident teaching or mentoring others?"
            ],

            "passion_exploration": [
                "What activities make you lose track of time because you're so engaged?",
                "When you daydream about your ideal life, what are you doing?",
                "What causes or issues in the world stir something deep within you?",
                "Think of a time when you felt most alive and energized. What were you doing?"
            ],

            "values_clarification": [
                "What principles or values guide your most important decisions?",
                "What would you want to be remembered for at the end of your life?",
                "What injustices or problems in the world motivate you to take action?",
                "What does 'making a difference' mean to you personally?"
            ],

            "synthesis": [
                "Looking at what we've discussed about your skills and passions, where do you see the strongest overlap?",
                "What patterns do you notice emerging from our conversation?",
                "If you could design a role that combines your best skills with your deepest passions, what would it look like?"
            ],

            "recommendations": [
                "Based on our journey together, I'd like to offer some insights about your spiritual gifts. Are you ready to explore these discoveries?",
                "What resonates most strongly with you from what we've uncovered?",
                "How might you begin to explore or develop these gifts further?"
            ]
        }

        return question_templates.get(stage, [])

    def get_next_question(self, previous_answers=None):
        """Get the next question based on current stage and progress"""
        current_stage_name = self.get_current_stage()

        if current_stage_name == "completed":
            return None

        questions = self.get_stage_questions(current_stage_name)
        current_progress = self.stage_progress[current_stage_name]
        question_index = current_progress["question_count"]

        # If we've asked all questions in this stage, move to next stage
        if question_index >= len(questions):
            self._advance_to_next_stage()
            return self.get_next_question(previous_answers)

        return questions[question_index]

    def process_response(self, user_response):
        """Process user response and store it appropriately"""
        current_stage_name = self.get_current_stage()

        if current_stage_name == "completed":
            return False

        # Store the response
        self.user_responses[current_stage_name].append({
            "response": user_response,
            "timestamp": datetime.now().isoformat(),
            "question_number": self.stage_progress[current_stage_name]["question_count"]
        })

        # Increment question count for this stage
        self.stage_progress[current_stage_name]["question_count"] += 1

        return True

    def _advance_to_next_stage(self):
        """Mark current stage as completed and advance to next"""
        if self.current_stage < len(self.stages):
            current_stage_name = self.stages[self.current_stage]
            self.stage_progress[current_stage_name]["completed"] = True
            self.current_stage += 1

    def build_contextual_prompt(self, stage, user_response=None):
        """Build context-aware prompt for the LLM"""
        # Gather all previous responses for context
        context_parts = []

        # Add user information from introduction
        if "introduction" in self.user_responses and self.user_responses["introduction"]:
            intro_responses = [r["response"] for r in self.user_responses["introduction"]]
            context_parts.append(f"User background: {' | '.join(intro_responses)}")

        # Add skills from skills assessment
        if "skills_assessment" in self.user_responses and self.user_responses["skills_assessment"]:
            skills_responses = [r["response"] for r in self.user_responses["skills_assessment"]]
            context_parts.append(f"Identified skills: {' | '.join(skills_responses)}")

        # Add passions from exploration
        if "passion_exploration" in self.user_responses and self.user_responses["passion_exploration"]:
            passion_responses = [r["response"] for r in self.user_responses["passion_exploration"]]
            context_parts.append(f"Core passions: {' | '.join(passion_responses)}")

        # Add values
        if "values_clarification" in self.user_responses and self.user_responses["values_clarification"]:
            values_responses = [r["response"] for r in self.user_responses["values_clarification"]]
            context_parts.append(f"Key values: {' | '.join(values_responses)}")

        # Build the contextual prompt
        context = "\n".join(context_parts) if context_parts else "Beginning of conversation"

        stage_guidance = {
            "introduction": "Focus on building rapport and understanding their motivation for spiritual discovery.",
            "skills_assessment": "Help them identify natural talents and developed abilities.",
            "passion_exploration": "Uncover what truly energizes and motivates them.",
            "values_clarification": "Explore their core beliefs and what drives their decisions.",
            "synthesis": "Help them see patterns and connections between skills, passions, and values.",
            "recommendations": "Provide insights about potential spiritual gifts based on all gathered information."
        }

        guidance = stage_guidance.get(stage, "Provide thoughtful, encouraging guidance.")

        prompt = f"""You are a wise spiritual guide helping someone discover their gifts and calling.

CURRENT STAGE: {stage.title()}
STAGE GUIDANCE: {guidance}

CONVERSATION CONTEXT:
{context}

USER'S LATEST RESPONSE: {user_response if user_response else "None yet"}

Respond with warmth and insight. {guidance} Ask thoughtful follow-up questions that help them go deeper. Keep your response concise but meaningful."""

        return prompt

    def get_session_summary(self):
        """Generate a summary of the discovery session"""
        summary = {
            "session_id": self.session_id,
            "current_stage": self.get_current_stage(),
            "progress": self.stage_progress,
            "total_responses": sum(len(responses) for responses in self.user_responses.values()),
            "completion_percentage": (self.current_stage / len(self.stages)) * 100
        }

        return summary

    def save_session(self, filename=None):
        """Save the discovery session to a JSON file"""
        if not filename:
            filename = f"discovery_sessions/discovery_{self.session_id}.json"

        os.makedirs("discovery_sessions", exist_ok=True)

        session_data = {
            "session_id": self.session_id,
            "created": datetime.now().isoformat(),
            "current_stage": self.current_stage,
            "stage_progress": self.stage_progress,
            "user_responses": self.user_responses,
            "summary": self.get_session_summary()
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

        return filename

    def load_session(self, filename):
        """Load a previous discovery session"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                session_data = json.load(f)

            self.session_id = session_data["session_id"]
            self.current_stage = session_data["current_stage"]
            self.stage_progress = session_data["stage_progress"]
            self.user_responses = session_data["user_responses"]

            return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error loading session: {e}")
            return False


class DiscoveryBot:
    """Enhanced bot with structured discovery journey"""

    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}"
        self.discovery_session = DiscoverySession()

        self.system_prompt = """You are a compassionate and wise spiritual guide specializing in helping people discover their spiritual gifts and life calling. You excel at asking thoughtful questions that help people connect their natural skills with their deepest passions and values."""

    def call_gemini(self, prompt):
        """Make API call to Gemini"""
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

            return "Sorry, I couldn't generate a response."

        except requests.exceptions.RequestException as e:
            return f"Error calling API: {e}"
        except KeyError as e:
            return f"Error parsing response: {e}"

    def start_discovery_journey(self):
        """Begin the structured discovery conversation"""
        print("=" * 70)
        print("🌟 Spiritual Discovery Journey 🌟")
        print("=" * 70)
        print("Welcome to your personal spiritual gifts discovery session!")
        print("I'll guide you through 6 stages to help uncover your unique calling.")
        print("\nStages: Introduction → Skills → Passions → Values → Synthesis → Recommendations")
        print("\nCommands: 'quit', 'save', 'progress', 'skip'")
        print("-" * 70)

        # Start with the first question
        first_question = self.discovery_session.get_next_question()
        if first_question:
            print(f"\nGuide: {first_question}")

        while True:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ['quit', 'exit', 'bye']:
                filename = self.discovery_session.save_session()
                print(f"\nGuide: Your discovery journey has been saved to {filename}")
                print("Take time to reflect on what we've explored. Your path continues to unfold! 🙏")
                break

            if user_input.lower() == 'save':
                filename = self.discovery_session.save_session()
                print(f"\nSession saved to {filename}")
                continue

            if user_input.lower() == 'progress':
                summary = self.discovery_session.get_session_summary()
                current_stage = summary["current_stage"]
                completion = summary["completion_percentage"]
                print(f"\n--- Discovery Progress ---")
                print(f"Current Stage: {current_stage.title()}")
                print(f"Overall Progress: {completion:.1f}%")
                print(f"Total Responses: {summary['total_responses']}")
                print("--- End Progress ---")
                continue

            if user_input.lower() == 'skip':
                print("\nSkipping to next stage...")
                self.discovery_session._advance_to_next_stage()
                next_question = self.discovery_session.get_next_question()
                if next_question:
                    print(f"\nGuide: {next_question}")
                else:
                    print("\nGuide: We've completed all discovery stages!")
                continue

            if not user_input:
                continue

            # Process the user's response
            success = self.discovery_session.process_response(user_input)
            if not success:
                print("\nGuide: Our discovery journey is complete! Thank you for sharing so openly.")
                break

            # Generate contextual response using AI
            current_stage = self.discovery_session.get_current_stage()
            contextual_prompt = self.discovery_session.build_contextual_prompt(current_stage, user_input)

            print("\nGuide: ", end="", flush=True)
            ai_response = self.call_gemini(contextual_prompt)
            print(ai_response)

            # Get next question if we're still in progress
            next_question = self.discovery_session.get_next_question()
            if next_question:
                print(f"\nNext: {next_question}")
            else:
                current_stage = self.discovery_session.get_current_stage()
                if current_stage == "completed":
                    print("\n🎉 Congratulations! You've completed your spiritual discovery journey!")
                    filename = self.discovery_session.save_session()
                    print(f"Your complete session has been saved to {filename}")
                    break


if __name__ == "__main__":
    try:
        bot = DiscoveryBot()
        bot.start_discovery_journey()
    except ValueError as e:
        print(f"Configuration error: {e}")
    except KeyboardInterrupt:
        print("\nGoodbye!")