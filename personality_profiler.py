#!/usr/bin/env python3
"""
Phase 4: Personality/Style Profiling System
Analyzes user communication patterns and adapts bot response style accordingly

Key Architecture Concepts:
1. Communication Style Detection: Analyze how user communicates
2. Personality Modeling: Build profile of user preferences
3. Adaptive Response Generation: Modify bot style to match user
4. Style Consistency: Maintain coherent personality throughout conversation
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class CommunicationStyle(Enum):
    ANALYTICAL = "analytical"      # Data-driven, logical, structured
    EXPRESSIVE = "expressive"      # Emotional, descriptive, enthusiastic
    PRACTICAL = "practical"       # Direct, action-oriented, concise
    REFLECTIVE = "reflective"     # Thoughtful, introspective, careful

class ResponseDepth(Enum):
    BRIEF = "brief"               # Short, to-the-point responses
    MODERATE = "moderate"         # Balanced detail level
    DETAILED = "detailed"         # Comprehensive, thorough responses

@dataclass
class PersonalityMarkers:
    """Indicators of user personality from communication patterns"""
    word_count_avg: float
    emotional_language_frequency: float
    question_asking_frequency: float
    concrete_vs_abstract_ratio: float
    uncertainty_indicators: float
    enthusiasm_markers: float

@dataclass
class CommunicationProfile:
    """User's communication style profile"""
    primary_style: CommunicationStyle
    secondary_style: Optional[CommunicationStyle]
    preferred_depth: ResponseDepth
    confidence: float  # How confident we are in this assessment
    markers: PersonalityMarkers
    adaptations: List[str]  # Specific adaptations to make

class PersonalityProfiler:
    """
    Analyzes user communication patterns and provides style adaptation guidance

    Architecture Pattern: User Modeling + Adaptive Interface
    - Tracks communication patterns
    - Builds user personality model
    - Provides style adaptation recommendations
    - Maintains consistency across conversation
    """

    def __init__(self):
        self.communication_samples: List[str] = []
        self.current_profile: Optional[CommunicationProfile] = None
        self.style_history: List[CommunicationStyle] = []

        # Analysis thresholds
        self.min_samples_for_profile = 3
        self.confidence_threshold = 0.6

    def analyze_communication_patterns(self, user_responses: List[str]) -> PersonalityMarkers:
        """
        Analyze user communication patterns to identify personality markers

        Architecture Concept: Communication Pattern Recognition
        """
        if not user_responses:
            return self._default_markers()

        # Calculate communication metrics
        total_words = sum(len(response.split()) for response in user_responses)
        avg_word_count = total_words / len(user_responses) if user_responses else 0

        # Emotional language analysis
        emotional_words = [
            'love', 'passionate', 'excited', 'energized', 'alive', 'frustrated', 'concerned',
            'worried', 'joyful', 'thrilled', 'overwhelmed', 'blessed', 'grateful', 'moved'
        ]

        emotional_count = 0
        for response in user_responses:
            response_lower = response.lower()
            emotional_count += sum(1 for word in emotional_words if word in response_lower)

        emotional_frequency = emotional_count / total_words if total_words > 0 else 0

        # Question asking frequency
        question_count = sum(response.count('?') for response in user_responses)
        question_frequency = question_count / len(user_responses) if user_responses else 0

        # Concrete vs abstract language
        concrete_words = [
            'specific', 'example', 'exactly', 'precisely', 'literally', 'actually',
            'definitely', 'clearly', 'obviously', 'specifically'
        ]
        abstract_words = [
            'generally', 'usually', 'often', 'sometimes', 'might', 'could',
            'possibly', 'perhaps', 'maybe', 'tend to', 'feel like'
        ]

        concrete_count = sum(
            sum(1 for word in concrete_words if word in response.lower())
            for response in user_responses
        )
        abstract_count = sum(
            sum(1 for word in abstract_words if word in response.lower())
            for response in user_responses
        )

        concrete_ratio = concrete_count / (concrete_count + abstract_count) if (concrete_count + abstract_count) > 0 else 0.5

        # Uncertainty indicators
        uncertainty_words = ['not sure', 'i think', 'maybe', 'perhaps', 'might be', 'could be', 'i guess']
        uncertainty_count = sum(
            sum(1 for phrase in uncertainty_words if phrase in response.lower())
            for response in user_responses
        )
        uncertainty_frequency = uncertainty_count / len(user_responses) if user_responses else 0

        # Enthusiasm markers
        enthusiasm_words = ['!', 'really', 'absolutely', 'definitely', 'totally', 'amazing', 'wonderful', 'incredible']
        enthusiasm_count = 0
        for response in user_responses:
            response_lower = response.lower()
            enthusiasm_count += sum(1 for word in enthusiasm_words if word in response_lower)
            enthusiasm_count += response.count('!')

        enthusiasm_frequency = enthusiasm_count / total_words if total_words > 0 else 0

        return PersonalityMarkers(
            word_count_avg=avg_word_count,
            emotional_language_frequency=emotional_frequency,
            question_asking_frequency=question_frequency,
            concrete_vs_abstract_ratio=concrete_ratio,
            uncertainty_indicators=uncertainty_frequency,
            enthusiasm_markers=enthusiasm_frequency
        )

    def _default_markers(self) -> PersonalityMarkers:
        """Default markers when insufficient data"""
        return PersonalityMarkers(
            word_count_avg=20.0,
            emotional_language_frequency=0.05,
            question_asking_frequency=0.2,
            concrete_vs_abstract_ratio=0.5,
            uncertainty_indicators=0.1,
            enthusiasm_markers=0.03
        )

    def determine_communication_style(self, markers: PersonalityMarkers) -> Tuple[CommunicationStyle, float]:
        """
        Determine primary communication style based on markers

        Architecture Concept: Pattern Classification
        """

        style_scores = {}

        # Analytical style indicators
        analytical_score = 0
        if markers.concrete_vs_abstract_ratio > 0.6:
            analytical_score += 0.3
        if markers.word_count_avg > 25:
            analytical_score += 0.2
        if markers.emotional_language_frequency < 0.03:
            analytical_score += 0.2
        if markers.question_asking_frequency > 0.3:
            analytical_score += 0.2
        if markers.uncertainty_indicators < 0.1:
            analytical_score += 0.1

        style_scores[CommunicationStyle.ANALYTICAL] = analytical_score

        # Expressive style indicators
        expressive_score = 0
        if markers.emotional_language_frequency > 0.01:  # Lower threshold
            expressive_score += 0.3
        if markers.enthusiasm_markers > 0.02:  # Lower threshold
            expressive_score += 0.3
        if markers.word_count_avg > 20:
            expressive_score += 0.2
        if markers.concrete_vs_abstract_ratio < 0.4:
            expressive_score += 0.2

        style_scores[CommunicationStyle.EXPRESSIVE] = expressive_score

        # Practical style indicators
        practical_score = 0
        if markers.word_count_avg < 15:
            practical_score += 0.3
        if markers.concrete_vs_abstract_ratio > 0.7:
            practical_score += 0.3
        if markers.emotional_language_frequency < 0.04:
            practical_score += 0.2
        if markers.question_asking_frequency < 0.2:
            practical_score += 0.2

        style_scores[CommunicationStyle.PRACTICAL] = practical_score

        # Reflective style indicators
        reflective_score = 0
        if markers.uncertainty_indicators > 0.15:
            reflective_score += 0.3
        if markers.word_count_avg > 30:
            reflective_score += 0.2
        if markers.question_asking_frequency > 0.25:
            reflective_score += 0.2
        if markers.concrete_vs_abstract_ratio < 0.5:
            reflective_score += 0.2
        if markers.emotional_language_frequency > 0.03 and markers.emotional_language_frequency < 0.08:
            reflective_score += 0.1

        style_scores[CommunicationStyle.REFLECTIVE] = reflective_score

        # Find primary style
        primary_style = max(style_scores.items(), key=lambda x: x[1])
        return primary_style[0], primary_style[1]

    def determine_response_depth(self, markers: PersonalityMarkers) -> ResponseDepth:
        """Determine preferred response depth"""

        if markers.word_count_avg < 12:
            return ResponseDepth.BRIEF
        elif markers.word_count_avg > 35:
            return ResponseDepth.DETAILED
        else:
            return ResponseDepth.MODERATE

    def build_communication_profile(self, user_responses: List[str]) -> Optional[CommunicationProfile]:
        """
        Build comprehensive communication profile

        Architecture Concept: User Model Construction
        """
        if len(user_responses) < self.min_samples_for_profile:
            return None

        # Analyze patterns
        markers = self.analyze_communication_patterns(user_responses)

        # Determine primary style
        primary_style, confidence = self.determine_communication_style(markers)

        # Determine secondary style (second highest score)
        # Simplified - would implement full secondary analysis in production

        # Determine preferred depth
        preferred_depth = self.determine_response_depth(markers)

        # Generate adaptation recommendations
        adaptations = self._generate_adaptations(primary_style, preferred_depth, markers)

        profile = CommunicationProfile(
            primary_style=primary_style,
            secondary_style=None,  # Simplified for now
            preferred_depth=preferred_depth,
            confidence=confidence,
            markers=markers,
            adaptations=adaptations
        )

        self.current_profile = profile
        return profile

    def _generate_adaptations(self, style: CommunicationStyle, depth: ResponseDepth, markers: PersonalityMarkers) -> List[str]:
        """Generate specific adaptations based on style"""

        adaptations = []

        # Style-based adaptations
        if style == CommunicationStyle.ANALYTICAL:
            adaptations.extend([
                "Use structured, logical responses",
                "Include specific examples and data points",
                "Avoid overly emotional language",
                "Ask clarifying questions for precision"
            ])
        elif style == CommunicationStyle.EXPRESSIVE:
            adaptations.extend([
                "Use warm, encouraging language",
                "Include emotional validation",
                "Use vivid, descriptive language",
                "Match their enthusiasm level"
            ])
        elif style == CommunicationStyle.PRACTICAL:
            adaptations.extend([
                "Keep responses concise and actionable",
                "Focus on concrete next steps",
                "Avoid excessive elaboration",
                "Be direct and clear"
            ])
        elif style == CommunicationStyle.REFLECTIVE:
            adaptations.extend([
                "Allow processing time between questions",
                "Use thoughtful, introspective language",
                "Validate their careful consideration",
                "Ask open-ended, reflective questions"
            ])

        # Depth-based adaptations
        if depth == ResponseDepth.BRIEF:
            adaptations.append("Keep responses shorter and more focused")
        elif depth == ResponseDepth.DETAILED:
            adaptations.append("Provide comprehensive, thorough responses")

        # Marker-based adaptations
        if markers.uncertainty_indicators > 0.2:
            adaptations.append("Provide reassurance and normalize uncertainty")

        if markers.enthusiasm_markers > 0.05:
            adaptations.append("Match and encourage their positive energy")

        return adaptations

    def get_style_guidance_for_llm(self) -> str:
        """
        Generate guidance for LLM to adapt its response style

        Architecture Concept: Style Transfer Instructions
        """
        if not self.current_profile:
            return "Respond naturally with warmth and insight."

        profile = self.current_profile
        guidance_parts = []

        # Primary style guidance
        style_instructions = {
            CommunicationStyle.ANALYTICAL: "Be logical, structured, and precise. Use specific examples. Ask clarifying questions.",
            CommunicationStyle.EXPRESSIVE: "Be warm, enthusiastic, and emotionally engaging. Use vivid language that matches their energy.",
            CommunicationStyle.PRACTICAL: "Be concise, direct, and action-oriented. Focus on practical insights and next steps.",
            CommunicationStyle.REFLECTIVE: "Be thoughtful, patient, and introspective. Allow space for contemplation and deeper reflection."
        }

        guidance_parts.append(f"COMMUNICATION STYLE: {style_instructions[profile.primary_style]}")

        # Depth guidance
        depth_instructions = {
            ResponseDepth.BRIEF: "Keep responses concise (2-3 sentences typically).",
            ResponseDepth.MODERATE: "Provide balanced detail (1-2 paragraphs typically).",
            ResponseDepth.DETAILED: "Offer comprehensive responses with thorough explanation."
        }

        guidance_parts.append(f"RESPONSE DEPTH: {depth_instructions[profile.preferred_depth]}")

        # Specific adaptations
        if profile.adaptations:
            guidance_parts.append(f"SPECIFIC ADAPTATIONS: {' | '.join(profile.adaptations[:3])}")

        return " ".join(guidance_parts)

    def update_profile(self, new_response: str):
        """Update profile with new response data"""
        self.communication_samples.append(new_response)

        # Rebuild profile if we have enough samples
        if len(self.communication_samples) >= self.min_samples_for_profile:
            self.build_communication_profile(self.communication_samples)

    def get_profile_summary(self) -> Dict:
        """Get summary of current profile for analysis"""
        if not self.current_profile:
            return {"status": "insufficient_data", "samples_needed": self.min_samples_for_profile - len(self.communication_samples)}

        profile = self.current_profile
        return {
            "primary_style": profile.primary_style.value,
            "preferred_depth": profile.preferred_depth.value,
            "confidence": profile.confidence,
            "markers": {
                "avg_word_count": profile.markers.word_count_avg,
                "emotional_frequency": profile.markers.emotional_language_frequency,
                "enthusiasm_level": profile.markers.enthusiasm_markers,
                "uncertainty_level": profile.markers.uncertainty_indicators
            },
            "adaptations_count": len(profile.adaptations),
            "total_samples": len(self.communication_samples)
        }


if __name__ == "__main__":
    # Test the personality profiler
    profiler = PersonalityProfiler()

    # Test with different communication styles
    analytical_responses = [
        "I need to understand exactly what this assessment measures and how the scoring works.",
        "Can you provide specific examples of what constitutes a 'teaching gift' versus other gifts?",
        "I've taken several assessments before and want to compare the methodologies used."
    ]

    expressive_responses = [
        "I'm so excited to discover my gifts! I've always felt drawn to helping others and it just makes my heart sing!",
        "When I see someone struggling, I just feel this overwhelming desire to come alongside them and encourage them.",
        "The idea of having spiritual gifts is absolutely amazing - I can't wait to see how God wants to use me!"
    ]

    practical_responses = [
        "I want to know my gifts so I can serve more effectively.",
        "What should I do next once I know my results?",
        "I'm here to get clear direction on where to focus my efforts."
    ]

    # Test analytical style
    print("ANALYTICAL PROFILE:")
    analytical_profile = profiler.build_communication_profile(analytical_responses)
    if analytical_profile:
        print(f"  Style: {analytical_profile.primary_style.value}")
        print(f"  Depth: {analytical_profile.preferred_depth.value}")
        print(f"  Confidence: {analytical_profile.confidence:.2f}")
        print(f"  Adaptations: {analytical_profile.adaptations[:2]}")

    # Reset and test expressive style
    profiler = PersonalityProfiler()
    print(f"\nEXPRESSIVE PROFILE:")
    expressive_profile = profiler.build_communication_profile(expressive_responses)
    if expressive_profile:
        print(f"  Style: {expressive_profile.primary_style.value}")
        print(f"  Depth: {expressive_profile.preferred_depth.value}")
        print(f"  Confidence: {expressive_profile.confidence:.2f}")
        print(f"  Style Guidance: {profiler.get_style_guidance_for_llm()}")

    # Test profile summary
    print(f"\nPROFILE SUMMARY:")
    summary = profiler.get_profile_summary()
    print(json.dumps(summary, indent=2))