#!/usr/bin/env python3
"""
Phase 4: Dynamic Questioning Engine
Implements adaptive conversation flow based on user response patterns

Key Architecture Concepts:
1. Response Analysis: Analyze user responses for emerging patterns
2. Conditional Flow Control: Branch conversation based on discoveries
3. Adaptive Question Generation: Create personalized follow-ups
4. Coverage Tracking: Ensure comprehensive assessment despite dynamic flow
"""

import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class QuestionType(Enum):
    STANDARD = "standard"           # Predetermined questions
    FOLLOW_UP = "follow_up"         # Based on previous response
    DEEP_DIVE = "deep_dive"         # Explore emerging theme
    CLARIFICATION = "clarification" # Clarify ambiguous responses
    SYNTHESIS = "synthesis"         # Connect patterns

@dataclass
class DynamicQuestion:
    """Represents a dynamically generated question"""
    question_text: str
    question_type: QuestionType
    target_theme: str
    reasoning: str  # Why this question was chosen
    priority: float  # 0.0 to 1.0, higher = more important

@dataclass
class ResponsePattern:
    """Identified pattern in user responses"""
    pattern_name: str
    confidence: float
    evidence: List[str]
    stage_first_seen: str
    implications: List[str]  # What this pattern suggests

class DynamicQuestioningEngine:
    """
    Advanced questioning system that adapts based on user responses

    Architecture Pattern: State Machine + Pattern Recognition
    - Tracks conversation state
    - Identifies response patterns
    - Generates adaptive questions
    - Maintains assessment coverage
    """

    def __init__(self):
        self.response_patterns: List[ResponsePattern] = []
        self.coverage_requirements: Dict[str, List[str]] = self._define_coverage_requirements()
        self.coverage_status: Dict[str, bool] = {area: False for area in self.coverage_requirements}
        self.dynamic_questions_asked: List[DynamicQuestion] = []

        # Question generation settings
        self.pattern_threshold = 0.7  # Minimum confidence to act on pattern
        self.max_follow_ups = 2       # Max follow-up questions per theme
        self.deep_dive_threshold = 0.8 # When to suggest deep exploration

    def _define_coverage_requirements(self) -> Dict[str, List[str]]:
        """
        Define minimum coverage areas for comprehensive assessment

        Architecture Note: This ensures dynamic flow doesn't miss critical areas
        """
        return {
            "natural_abilities": [
                "What comes easily to you that others find difficult?",
                "What skills do people compliment you on most often?",
                "In what areas do others seek your help or advice?"
            ],
            "energy_sources": [
                "What activities energize rather than drain you?",
                "When do you feel most alive and engaged?",
                "What would you do for free because you love it so much?"
            ],
            "core_values": [
                "What principles guide your important decisions?",
                "What would you want to be remembered for?",
                "What injustices or problems motivate you to action?"
            ],
            "impact_desires": [
                "How do you want to make a difference in the world?",
                "What legacy do you hope to leave?",
                "Who do you most want to help or serve?"
            ]
        }

    def analyze_response_patterns(self, user_responses: Dict[str, List[Dict]], current_stage: str) -> List[ResponsePattern]:
        """
        Analyze user responses to identify emerging patterns

        Architecture Concept: Pattern Recognition for Adaptive Flow
        """
        patterns = []

        # Collect all responses as text
        all_responses = []
        for stage_responses in user_responses.values():
            for response_obj in stage_responses:
                all_responses.append(response_obj.get('response', ''))

        response_text = ' '.join(all_responses).lower()

        # Pattern detection rules
        pattern_rules = {
            'strong_teaching_indicators': {
                'keywords': ['teach', 'explain', 'mentor', 'guide', 'help others learn', 'break down'],
                'phrases': ['people come to me', 'i love helping others understand', 'explaining'],
                'threshold': 0.7
            },
            'leadership_emergence': {
                'keywords': ['lead', 'organize', 'vision', 'inspire', 'motivate others', 'take charge'],
                'phrases': ['others follow', 'i see the big picture', 'rally people'],
                'threshold': 0.7
            },
            'service_orientation': {
                'keywords': ['serve', 'help', 'support', 'care', 'assist', 'come alongside'],
                'phrases': ['behind the scenes', 'prefer to support', 'help others succeed'],
                'threshold': 0.6
            },
            'creative_expression': {
                'keywords': ['create', 'design', 'artistic', 'beauty', 'express', 'imagine'],
                'phrases': ['creative outlet', 'artistic expression', 'beauty matters'],
                'threshold': 0.6
            },
            'justice_passion': {
                'keywords': ['justice', 'fair', 'equality', 'advocate', 'stand up', 'rights'],
                'phrases': ['not fair', 'speak up for', 'injustice bothers me'],
                'threshold': 0.7
            }
        }

        for pattern_name, rules in pattern_rules.items():
            evidence = []
            score = 0

            # Check keywords
            for keyword in rules['keywords']:
                if keyword in response_text:
                    evidence.append(f"Mentioned: {keyword}")
                    score += 0.2

            # Check phrases
            for phrase in rules['phrases']:
                if phrase in response_text:
                    evidence.append(f"Said: {phrase}")
                    score += 0.3

            # Normalize score
            confidence = min(score, 1.0)

            if confidence >= rules['threshold'] and evidence:
                pattern = ResponsePattern(
                    pattern_name=pattern_name,
                    confidence=confidence,
                    evidence=evidence,
                    stage_first_seen=current_stage,
                    implications=self._get_pattern_implications(pattern_name)
                )
                patterns.append(pattern)

        # Update stored patterns
        self.response_patterns.extend(patterns)
        return patterns

    def _get_pattern_implications(self, pattern_name: str) -> List[str]:
        """Get implications of identified patterns for question generation"""
        implications_map = {
            'strong_teaching_indicators': [
                'Explore specific teaching experiences',
                'Ask about satisfaction from others learning',
                'Investigate formal vs informal teaching preferences'
            ],
            'leadership_emergence': [
                'Explore vision-casting experiences',
                'Ask about team dynamics and motivation',
                'Investigate leadership style preferences'
            ],
            'service_orientation': [
                'Explore behind-the-scenes contributions',
                'Ask about satisfaction from supporting others',
                'Investigate preferred ways to help'
            ],
            'creative_expression': [
                'Explore artistic outlets and mediums',
                'Ask about role of beauty in life',
                'Investigate creative problem-solving'
            ],
            'justice_passion': [
                'Explore specific justice issues that matter',
                'Ask about advocacy experiences',
                'Investigate ways they want to create change'
            ]
        }
        return implications_map.get(pattern_name, [])

    def generate_next_question(self, user_responses: Dict, current_stage: str, last_response: str) -> DynamicQuestion:
        """
        Generate the next question based on conversation state and patterns

        Architecture Concept: Adaptive Question Generation
        """

        # Analyze current patterns
        new_patterns = self.analyze_response_patterns(user_responses, current_stage)

        # Check for strong patterns that warrant immediate follow-up
        for pattern in new_patterns:
            if pattern.confidence >= self.deep_dive_threshold:
                deep_dive_question = self._generate_deep_dive_question(pattern, last_response)
                if deep_dive_question:
                    return deep_dive_question

        # Generate follow-up based on immediate response
        follow_up = self._generate_follow_up_question(last_response, current_stage)
        if follow_up:
            return follow_up

        # Check coverage requirements
        uncovered_area = self._find_uncovered_area(user_responses)
        if uncovered_area:
            return self._generate_coverage_question(uncovered_area)

        # Generate synthesis question if patterns are strong
        if len([p for p in self.response_patterns if p.confidence >= 0.7]) >= 2:
            return self._generate_synthesis_question()

        # Default to standard stage question
        return self._generate_standard_question(current_stage)

    def _generate_deep_dive_question(self, pattern: ResponsePattern, last_response: str) -> Optional[DynamicQuestion]:
        """Generate questions to explore strong patterns more deeply"""

        deep_dive_templates = {
            'strong_teaching_indicators': [
                "You've mentioned teaching/explaining several times - can you tell me about a specific time when you helped someone understand something complex?",
                "It sounds like you have a natural teaching gift. What do you find most rewarding about helping others learn?",
                "When you're explaining something to someone, what approach do you naturally take?"
            ],
            'leadership_emergence': [
                "I notice leadership themes in what you're sharing. Can you describe a time when you naturally took charge of a situation?",
                "What happens when you're in a group and no clear direction exists?",
                "How do you typically motivate or inspire others?"
            ],
            'service_orientation': [
                "You seem drawn to supporting and helping others. What's your favorite way to serve?",
                "Tell me about a time when you helped someone succeed - what was that like for you?",
                "Do you prefer to help from behind the scenes or more visibly?"
            ]
        }

        templates = deep_dive_templates.get(pattern.pattern_name, [])
        if not templates:
            return None

        # Choose template based on what hasn't been asked
        template = templates[0]  # Simplified selection

        return DynamicQuestion(
            question_text=template,
            question_type=QuestionType.DEEP_DIVE,
            target_theme=pattern.pattern_name,
            reasoning=f"Strong {pattern.pattern_name} pattern detected (confidence: {pattern.confidence:.2f})",
            priority=0.9
        )

    def _generate_follow_up_question(self, last_response: str, stage: str) -> Optional[DynamicQuestion]:
        """Generate contextual follow-up based on immediate response"""

        response_lower = last_response.lower()

        # Follow-up triggers
        follow_up_rules = [
            {
                'triggers': ['i love', 'passionate about', 'deeply care'],
                'question': "What specifically about that resonates so deeply with you?",
                'reasoning': "User expressed strong passion"
            },
            {
                'triggers': ['difficult', 'challenging', 'struggle with'],
                'question': "Even though it's challenging, what draws you to persist with it?",
                'reasoning': "User mentioned difficulty but continued engagement"
            },
            {
                'triggers': ['people come to me', 'others seek me out', 'friends ask me'],
                'question': "What do you think it is about you that makes people naturally turn to you for this?",
                'reasoning': "User mentioned others recognizing their ability"
            },
            {
                'triggers': ['started', 'began', 'initiated'],
                'question': "What motivated you to take that first step?",
                'reasoning': "User mentioned taking initiative"
            }
        ]

        for rule in follow_up_rules:
            if any(trigger in response_lower for trigger in rule['triggers']):
                return DynamicQuestion(
                    question_text=rule['question'],
                    question_type=QuestionType.FOLLOW_UP,
                    target_theme=stage,
                    reasoning=rule['reasoning'],
                    priority=0.7
                )

        return None

    def _find_uncovered_area(self, user_responses: Dict) -> Optional[str]:
        """Find areas that haven't been adequately covered"""

        # Simple coverage check - in production would be more sophisticated
        covered_themes = set()
        all_text = ' '.join([
            resp.get('response', '')
            for stage_responses in user_responses.values()
            for resp in stage_responses
        ]).lower()

        # Check what themes are covered
        theme_indicators = {
            'natural_abilities': ['good at', 'excel', 'talented', 'naturally', 'easily'],
            'energy_sources': ['energizes', 'love', 'enjoy', 'alive', 'passionate'],
            'core_values': ['value', 'important', 'principle', 'believe', 'matters'],
            'impact_desires': ['difference', 'change', 'help', 'impact', 'legacy']
        }

        for theme, indicators in theme_indicators.items():
            if any(indicator in all_text for indicator in indicators):
                covered_themes.add(theme)

        # Return first uncovered area
        for area in self.coverage_requirements:
            if area not in covered_themes:
                return area

        return None

    def _generate_coverage_question(self, uncovered_area: str) -> DynamicQuestion:
        """Generate question to cover missing area"""
        questions = self.coverage_requirements[uncovered_area]

        return DynamicQuestion(
            question_text=questions[0],  # Take first question for simplicity
            question_type=QuestionType.STANDARD,
            target_theme=uncovered_area,
            reasoning=f"Ensuring coverage of {uncovered_area}",
            priority=0.6
        )

    def _generate_synthesis_question(self) -> DynamicQuestion:
        """Generate question that helps connect discovered patterns"""

        synthesis_questions = [
            "Looking at what you've shared about your strengths and passions, where do you see the strongest connections?",
            "What patterns are you noticing about what energizes you and what you're naturally good at?",
            "If you could design a role that perfectly combined your gifts and passions, what would it look like?",
            "How do you think your natural abilities could serve your deepest passions?"
        ]

        return DynamicQuestion(
            question_text=synthesis_questions[0],
            question_type=QuestionType.SYNTHESIS,
            target_theme="pattern_connection",
            reasoning="Multiple strong patterns identified - time to synthesize",
            priority=0.8
        )

    def _generate_standard_question(self, stage: str) -> DynamicQuestion:
        """Fallback to standard stage-appropriate question"""

        standard_questions = {
            'introduction': "Tell me what brought you here to explore your spiritual gifts today?",
            'skills_assessment': "What's something you do that others find difficult but comes naturally to you?",
            'passion_exploration': "What activities or causes make you feel most alive and engaged?",
            'values_clarification': "What principles or values guide your most important decisions?"
        }

        question = standard_questions.get(stage, "Tell me more about your experiences.")

        return DynamicQuestion(
            question_text=question,
            question_type=QuestionType.STANDARD,
            target_theme=stage,
            reasoning="Standard stage question",
            priority=0.5
        )

    def should_continue_current_stage(self, stage: str, response_count: int) -> bool:
        """
        Determine if we should continue in current stage or advance

        Architecture Concept: Dynamic Stage Progression
        """

        # Minimum responses per stage
        min_responses = {'introduction': 1, 'skills_assessment': 2, 'passion_exploration': 2, 'values_clarification': 1}

        if response_count < min_responses.get(stage, 1):
            return True

        # Continue if we have strong patterns to explore
        recent_patterns = [p for p in self.response_patterns if p.confidence >= 0.8]
        if recent_patterns and response_count < 4:  # Max 4 per stage
            return True

        return False

    def get_questioning_summary(self) -> Dict[str, Any]:
        """Get summary of dynamic questioning state"""
        return {
            "patterns_identified": len(self.response_patterns),
            "high_confidence_patterns": len([p for p in self.response_patterns if p.confidence >= 0.8]),
            "dynamic_questions_asked": len(self.dynamic_questions_asked),
            "coverage_status": self.coverage_status,
            "strongest_patterns": [
                {"name": p.pattern_name, "confidence": p.confidence}
                for p in sorted(self.response_patterns, key=lambda x: x.confidence, reverse=True)[:3]
            ]
        }


if __name__ == "__main__":
    # Test the dynamic questioning engine
    engine = DynamicQuestioningEngine()

    # Simulate user responses
    test_responses = {
        'introduction': [
            {'response': 'I love helping people discover their potential and often teach others'}
        ],
        'skills_assessment': [
            {'response': 'People often come to me for advice and I excel at explaining complex concepts'},
            {'response': 'I find it easy to break down difficult topics so others can understand and I really enjoy teaching'}
        ]
    }

    # Test pattern analysis
    patterns = engine.analyze_response_patterns(test_responses, 'skills_assessment')
    print("IDENTIFIED PATTERNS:")
    for pattern in patterns:
        print(f"  {pattern.pattern_name}: {pattern.confidence:.2f} confidence")
        print(f"    Evidence: {pattern.evidence}")

    # Test dynamic question generation
    next_question = engine.generate_next_question(
        test_responses,
        'skills_assessment',
        'I find it easy to break down difficult topics so others can understand'
    )

    print(f"\nNEXT DYNAMIC QUESTION:")
    print(f"  Type: {next_question.question_type.value}")
    print(f"  Question: {next_question.question_text}")
    print(f"  Reasoning: {next_question.reasoning}")
    print(f"  Priority: {next_question.priority}")

    print(f"\nQUESTIONING SUMMARY:")
    print(json.dumps(engine.get_questioning_summary(), indent=2))