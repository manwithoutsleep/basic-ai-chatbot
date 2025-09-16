#!/usr/bin/env python3
"""
Phase 4: Context-Aware Response System
Manages conversation context and provides intelligent context injection for LLM calls
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

@dataclass
class ContextInsight:
    """Represents a key insight discovered during conversation"""
    content: str
    stage: str
    confidence: float  # 0.0 to 1.0
    timestamp: str
    insight_type: str  # 'skill', 'passion', 'value', 'gift_indicator', 'pattern'

@dataclass
class ConversationTheme:
    """Tracks emerging themes across the conversation"""
    theme_name: str
    evidence: List[str]  # Quotes/responses that support this theme
    strength: float  # How strongly this theme appears
    first_mentioned: str  # Stage where it first appeared

class EnhancedContextManager:
    """
    Advanced context management for AI chatbot architecture

    Key Architecture Concepts:
    1. Context Windowing: Manage how much conversation history to include
    2. Insight Extraction: Identify and store key discoveries
    3. Theme Tracking: Follow patterns across multiple responses
    4. Intelligent Context Injection: Provide relevant context without overwhelming the LLM
    """

    def __init__(self):
        self.insights: List[ContextInsight] = []
        self.themes: Dict[str, ConversationTheme] = {}
        self.conversation_timeline: List[Dict] = []
        self.current_stage = "introduction"

        # Context management settings
        self.max_context_window = 8  # Keep last 8 exchanges in full detail
        self.insight_threshold = 0.6  # Minimum confidence to store as insight

    def add_exchange(self, user_input: str, bot_response: str, stage: str):
        """
        Add a conversation exchange and extract insights

        Architecture Note: This is where we implement 'memory' in a stateless LLM system
        """
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "stage": stage,
            "user_input": user_input,
            "bot_response": bot_response,
            "exchange_id": len(self.conversation_timeline)
        }

        self.conversation_timeline.append(exchange)
        self.current_stage = stage

        # Extract insights from this exchange
        self._extract_insights_from_exchange(user_input, stage)

        # Update themes
        self._update_themes(user_input, stage)

        # Maintain context window size
        self._manage_context_window()

    def _extract_insights_from_exchange(self, user_input: str, stage: str):
        """
        Extract key insights from user input using pattern recognition

        Architecture Concept: This simulates what an LLM could do with semantic analysis
        In a more advanced system, we'd use the LLM itself to identify insights
        """

        # Insight patterns - in real implementation, this would use LLM analysis
        insight_patterns = {
            'strong_skill_indicator': [
                ('people often come to me', 0.8),
                ('i excel at', 0.8),
                ('i\'m naturally good at', 0.9),
                ('others seek me out', 0.8),
                ('i find it easy to', 0.7)
            ],
            'passion_indicator': [
                ('i love', 0.8),
                ('makes me feel alive', 0.9),
                ('lose track of time', 0.9),
                ('deeply passionate about', 0.9),
                ('stirs my heart', 0.8)
            ],
            'value_indicator': [
                ('important to me', 0.7),
                ('i believe in', 0.7),
                ('guides my decisions', 0.8),
                ('core value', 0.9)
            ],
            'gift_indicator': [
                ('calling', 0.8),
                ('ministry', 0.8),
                ('gifted in', 0.9),
                ('spiritual gift', 0.9)
            ]
        }

        user_lower = user_input.lower()

        for insight_type, patterns in insight_patterns.items():
            for pattern, confidence in patterns:
                if pattern in user_lower:
                    insight = ContextInsight(
                        content=user_input,
                        stage=stage,
                        confidence=confidence,
                        timestamp=datetime.now().isoformat(),
                        insight_type=insight_type
                    )

                    if confidence >= self.insight_threshold:
                        self.insights.append(insight)

    def _update_themes(self, user_input: str, stage: str):
        """
        Track recurring themes across the conversation

        Architecture Note: Theme tracking helps identify patterns that span multiple exchanges
        """

        # Theme keywords (simplified - would use semantic analysis in production)
        theme_keywords = {
            'teaching': ['teach', 'explain', 'mentor', 'guide', 'instruct', 'help others learn'],
            'leadership': ['lead', 'direct', 'manage', 'organize', 'vision', 'inspire others'],
            'helping': ['help', 'serve', 'support', 'assist', 'care for', 'come alongside'],
            'creativity': ['create', 'design', 'artistic', 'express', 'beauty', 'innovation'],
            'justice': ['justice', 'fairness', 'equality', 'advocate', 'stand up for', 'rights'],
            'people_focus': ['people', 'relationships', 'community', 'connection', 'social']
        }

        user_lower = user_input.lower()

        for theme_name, keywords in theme_keywords.items():
            matches = [kw for kw in keywords if kw in user_lower]

            if matches:
                if theme_name not in self.themes:
                    self.themes[theme_name] = ConversationTheme(
                        theme_name=theme_name,
                        evidence=[user_input],
                        strength=1.0,
                        first_mentioned=stage
                    )
                else:
                    # Strengthen existing theme
                    self.themes[theme_name].evidence.append(user_input)
                    self.themes[theme_name].strength += 0.5

                    # Cap strength at reasonable level
                    if self.themes[theme_name].strength > 5.0:
                        self.themes[theme_name].strength = 5.0

    def _manage_context_window(self):
        """
        Keep conversation timeline within manageable size

        Architecture Concept: Context windowing prevents LLM prompts from becoming too long
        """
        if len(self.conversation_timeline) > self.max_context_window:
            # Keep the most recent exchanges, summarize older ones
            recent_exchanges = self.conversation_timeline[-self.max_context_window:]
            self.conversation_timeline = recent_exchanges

    def build_context_for_llm(self, current_user_input: str = None) -> str:
        """
        Build intelligent context string for LLM prompt

        Architecture Concept: Context injection - providing relevant background without overwhelming the model
        """
        context_parts = []

        # Add key insights summary
        if self.insights:
            high_confidence_insights = [i for i in self.insights if i.confidence >= 0.8]
            if high_confidence_insights:
                context_parts.append("KEY INSIGHTS DISCOVERED:")
                for insight in high_confidence_insights[-3:]:  # Last 3 high-confidence insights
                    context_parts.append(f"  • {insight.stage}: {insight.content[:100]}...")

        # Add strongest themes
        if self.themes:
            strong_themes = [(name, theme) for name, theme in self.themes.items() if theme.strength >= 2.0]
            strong_themes.sort(key=lambda x: x[1].strength, reverse=True)

            if strong_themes:
                context_parts.append("\nEMERGING THEMES:")
                for theme_name, theme in strong_themes[:3]:  # Top 3 themes
                    context_parts.append(f"  • {theme_name.title()}: Mentioned {len(theme.evidence)} times (strength: {theme.strength:.1f})")

        # Add recent conversation
        context_parts.append("\nRECENT CONVERSATION:")
        for exchange in self.conversation_timeline[-3:]:  # Last 3 exchanges
            context_parts.append(f"  User: {exchange['user_input']}")
            context_parts.append(f"  Guide: {exchange['bot_response'][:150]}...")

        # Add current input if provided
        if current_user_input:
            context_parts.append(f"\nCURRENT USER INPUT: {current_user_input}")

        return "\n".join(context_parts)

    def get_contextual_guidance(self, stage: str) -> str:
        """
        Provide stage-specific guidance that considers conversation context

        Architecture Concept: Adaptive guidance based on discovered patterns
        """
        guidance_parts = []

        # Base guidance for stage
        stage_guidance = {
            "introduction": "Build rapport and understand their motivation for discovery",
            "skills_assessment": "Help identify natural talents and developed abilities",
            "passion_exploration": "Uncover what truly energizes and motivates them",
            "values_clarification": "Explore core beliefs and decision-making drivers",
            "synthesis": "Help connect patterns between skills, passions, and values",
            "recommendations": "Provide insights about spiritual gifts based on all information"
        }

        base_guidance = stage_guidance.get(stage, "Provide thoughtful guidance")
        guidance_parts.append(f"STAGE GUIDANCE: {base_guidance}")

        # Add contextual guidance based on themes
        if self.themes:
            strongest_theme = max(self.themes.values(), key=lambda t: t.strength)
            if strongest_theme.strength >= 2.0:
                guidance_parts.append(f"CONTEXT: User shows strong {strongest_theme.theme_name} theme - explore this further")

        # Add insight-based guidance
        recent_insights = [i for i in self.insights if i.stage == stage and i.confidence >= 0.7]
        if recent_insights:
            guidance_parts.append("RECENT INSIGHTS: Build on what they've shared about their strengths")

        return " | ".join(guidance_parts)

    def should_suggest_deep_dive(self, theme: str) -> bool:
        """
        Determine if we should suggest exploring a theme more deeply

        Architecture Concept: Dynamic conversation steering based on emerging patterns
        """
        if theme in self.themes:
            theme_obj = self.themes[theme]
            # Suggest deep dive if theme is strong and appeared in multiple stages
            return theme_obj.strength >= 2.5 and len(theme_obj.evidence) >= 3
        return False

    def get_conversation_summary(self) -> Dict[str, Any]:
        """Generate summary of conversation state for debugging/analysis"""
        return {
            "total_exchanges": len(self.conversation_timeline),
            "current_stage": self.current_stage,
            "insights_count": len(self.insights),
            "themes": {name: {"strength": theme.strength, "evidence_count": len(theme.evidence)}
                      for name, theme in self.themes.items()},
            "high_confidence_insights": len([i for i in self.insights if i.confidence >= 0.8])
        }

    def save_context(self, filename: str):
        """Save context state for session persistence"""
        context_data = {
            "insights": [
                {
                    "content": i.content,
                    "stage": i.stage,
                    "confidence": i.confidence,
                    "timestamp": i.timestamp,
                    "insight_type": i.insight_type
                } for i in self.insights
            ],
            "themes": {
                name: {
                    "theme_name": theme.theme_name,
                    "evidence": theme.evidence,
                    "strength": theme.strength,
                    "first_mentioned": theme.first_mentioned
                } for name, theme in self.themes.items()
            },
            "conversation_timeline": self.conversation_timeline,
            "current_stage": self.current_stage
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(context_data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # Test the context manager
    manager = EnhancedContextManager()

    # Simulate conversation
    manager.add_exchange(
        "Hi, I'm Sarah. I love helping people discover their potential and often teach others",
        "That's wonderful! Teaching and helping others discover potential are beautiful gifts.",
        "introduction"
    )

    manager.add_exchange(
        "People often come to me for advice and I excel at explaining complex concepts simply",
        "It sounds like you have natural teaching abilities. Tell me more about this.",
        "skills_assessment"
    )

    # Test context building
    context = manager.build_context_for_llm("I lose track of time when mentoring someone")
    print("CONTEXT FOR LLM:")
    print(context)

    print("\nCONVERSATION SUMMARY:")
    print(json.dumps(manager.get_conversation_summary(), indent=2))