#!/usr/bin/env python3
"""
Phase 5: Streamlit Web Interface for Spiritual Gifts Discovery
Converts our CLI intelligence system into an engaging web application

Key Web Architecture Concepts:
1. Session State Management: Preserve conversation across web interactions
2. Progressive UI Updates: Show AI insights as they develop
3. Component-Based UI: Modular interface elements
4. State Synchronization: Keep web state aligned with AI systems
"""

import streamlit as st
import json
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Import our Phase 4 intelligence systems
from enhanced_discovery_bot import EnhancedSpiritualDiscoveryBot
from context_manager import EnhancedContextManager
from dynamic_questioning import DynamicQuestioningEngine
from personality_profiler import PersonalityProfiler
from scoring_system import SpiritualGiftsAssessment

# Import Phase 5 visualization components
from visualization_components import SpiritualGiftsVisualizer, ConversationExporter, render_visualization_dashboard, render_export_options

# Configure page
st.set_page_config(
    page_title="Spiritual Gifts Discovery",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """
    Initialize Streamlit session state for our AI systems

    Architecture Concept: Session State Management
    Web apps are stateless by default, but our AI needs conversation memory
    """
    if 'initialized' not in st.session_state:
        # Initialize AI systems
        st.session_state.context_manager = EnhancedContextManager()
        st.session_state.dynamic_questioner = DynamicQuestioningEngine()
        st.session_state.personality_profiler = PersonalityProfiler()
        st.session_state.assessor = SpiritualGiftsAssessment()

        # Initialize conversation state
        st.session_state.conversation_history = []
        st.session_state.current_stage = "introduction"
        st.session_state.total_exchanges = 0
        st.session_state.session_start = datetime.now()

        # Initialize UI state
        st.session_state.show_insights = False
        st.session_state.show_personality = False
        st.session_state.show_analytics = False
        st.session_state.show_export = False
        st.session_state.discovery_complete = False

        st.session_state.initialized = True

def create_sidebar():
    """
    Create intelligent sidebar with real-time insights

    Architecture Concept: Progressive UI Updates
    Show AI analysis as it develops, not just at the end
    """
    with st.sidebar:
        st.header("🧠 AI Insights")

        # Progress indicator
        progress = min(st.session_state.total_exchanges / 15, 1.0)  # Estimate 15 exchanges for completion
        st.progress(progress, text=f"Discovery Progress: {progress*100:.0f}%")

        # Context insights
        if hasattr(st.session_state, 'context_manager'):
            insights_count = len(st.session_state.context_manager.insights)
            themes_count = len(st.session_state.context_manager.themes)

            st.metric("Insights Discovered", insights_count)
            st.metric("Themes Identified", themes_count)

            # Show top themes
            if st.session_state.context_manager.themes:
                st.subheader("🎯 Emerging Themes")
                sorted_themes = sorted(
                    st.session_state.context_manager.themes.items(),
                    key=lambda x: x[1].strength,
                    reverse=True
                )[:3]

                for theme_name, theme in sorted_themes:
                    st.write(f"**{theme_name.title()}**: {theme.strength:.1f} strength")

        # Personality profile
        if hasattr(st.session_state, 'personality_profiler'):
            profile = st.session_state.personality_profiler.current_profile
            if profile:
                st.subheader("🎨 Communication Style")
                st.write(f"**Style**: {profile.primary_style.value.title()}")
                st.write(f"**Confidence**: {profile.confidence:.2f}")

                # Style characteristics
                if profile.primary_style.value == 'expressive':
                    st.write("🌟 Warm, enthusiastic, emotional")
                elif profile.primary_style.value == 'analytical':
                    st.write("🔍 Logical, structured, precise")
                elif profile.primary_style.value == 'practical':
                    st.write("⚡ Direct, action-oriented, concise")
                elif profile.primary_style.value == 'reflective':
                    st.write("💭 Thoughtful, introspective, careful")

        # Action buttons
        st.divider()
        if st.button("📊 Show Detailed Insights"):
            st.session_state.show_insights = True

        if st.button("🎭 Show Personality Analysis"):
            st.session_state.show_personality = True

        if st.button("📊 Analytics Dashboard"):
            st.session_state.show_analytics = True

        if st.button("💾 Export Options"):
            st.session_state.show_export = True

def create_conversation_interface():
    """
    Main conversation interface with intelligent responses

    Architecture Concept: Real-time AI Integration
    """
    st.header("✨ Spiritual Gifts Discovery Journey")

    # Introduction
    if st.session_state.total_exchanges == 0:
        st.markdown("""
        Welcome to your **intelligent** spiritual gifts discovery experience!

        This enhanced system will:
        - 🧠 **Remember** and reference your previous insights
        - 🎯 **Adapt** questions based on patterns it discovers
        - 🎨 **Match** its communication style to your preferences
        - 📊 **Provide** real-time analysis of your responses

        Let's begin your personalized journey of discovery!
        """)

    # Conversation history
    if st.session_state.conversation_history:
        st.subheader("💬 Our Conversation")

        for i, exchange in enumerate(st.session_state.conversation_history):
            # User message
            with st.chat_message("user"):
                st.write(exchange['user_input'])

            # Bot response
            with st.chat_message("assistant"):
                st.write(exchange['bot_response'])

                # Show AI reasoning for recent exchanges
                if i >= len(st.session_state.conversation_history) - 2:
                    if 'ai_reasoning' in exchange:
                        with st.expander("🔍 AI Analysis", expanded=False):
                            st.write(exchange['ai_reasoning'])

    # Input for next response
    st.subheader("Your Response")

    # Get next question intelligently
    next_question = get_next_intelligent_question()
    if next_question:
        st.info(f"**Guide**: {next_question}")

    # User input
    user_input = st.text_area(
        "Share your thoughts:",
        height=100,
        placeholder="Type your response here..."
    )

    # Submit button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("💬 Submit Response", type="primary", disabled=not user_input.strip()):
            process_user_response(user_input.strip())
            st.rerun()

    with col2:
        if st.button("🔄 Get Different Question"):
            # Force generate a different question type
            force_new_question()
            st.rerun()

def get_next_intelligent_question():
    """Generate next question using our dynamic questioning system"""
    if not hasattr(st.session_state, 'dynamic_questioner'):
        return "What brought you here to explore your spiritual gifts today?"

    # Build user responses in the format our system expects
    user_responses = {'introduction': [], 'skills_assessment': [], 'passion_exploration': [], 'values_clarification': []}

    for exchange in st.session_state.conversation_history:
        # Determine stage based on exchange count (simplified)
        if len(st.session_state.conversation_history) <= 2:
            stage = 'introduction'
        elif len(st.session_state.conversation_history) <= 6:
            stage = 'skills_assessment'
        elif len(st.session_state.conversation_history) <= 10:
            stage = 'passion_exploration'
        else:
            stage = 'values_clarification'

        user_responses[stage].append({'response': exchange['user_input']})

    # Generate dynamic question
    if st.session_state.conversation_history:
        last_response = st.session_state.conversation_history[-1]['user_input']
        dynamic_question = st.session_state.dynamic_questioner.generate_next_question(
            user_responses,
            st.session_state.current_stage,
            last_response
        )
        return dynamic_question.question_text
    else:
        return "Hello! I'm excited to guide you on this journey of self-discovery. What's your name, and what drew you to explore your spiritual gifts today?"

def process_user_response(user_input):
    """
    Process user response through all AI systems

    Architecture Concept: System Orchestration
    Coordinate multiple AI systems for coherent experience
    """

    # Generate AI response with context and style adaptation
    ai_response, ai_reasoning = generate_intelligent_response(user_input)

    # Update all AI systems
    st.session_state.context_manager.add_exchange(
        user_input, ai_response, st.session_state.current_stage
    )

    st.session_state.personality_profiler.update_profile(user_input)

    # Store conversation
    exchange = {
        'user_input': user_input,
        'bot_response': ai_response,
        'ai_reasoning': ai_reasoning,
        'timestamp': datetime.now().isoformat(),
        'stage': st.session_state.current_stage
    }

    st.session_state.conversation_history.append(exchange)
    st.session_state.total_exchanges += 1

    # Update stage if needed
    if st.session_state.total_exchanges >= 12:  # After sufficient exchanges
        st.session_state.current_stage = "synthesis"
        if st.session_state.total_exchanges >= 15:
            st.session_state.discovery_complete = True

def generate_intelligent_response(user_input):
    """Generate AI response with full intelligence integration"""

    # Build context
    context = st.session_state.context_manager.build_context_for_llm(user_input)

    # Get style guidance
    style_guidance = st.session_state.personality_profiler.get_style_guidance_for_llm()

    # Generate reasoning for transparency
    reasoning_parts = []

    # Analyze for patterns
    if len(st.session_state.conversation_history) >= 2:
        all_responses = [ex['user_input'] for ex in st.session_state.conversation_history]
        all_responses.append(user_input)

        # Use our pattern analysis
        user_responses_dict = {'all': [{'response': r} for r in all_responses]}
        patterns = st.session_state.dynamic_questioner.analyze_response_patterns(
            user_responses_dict, st.session_state.current_stage
        )

        if patterns:
            strong_patterns = [p for p in patterns if p.confidence >= 0.7]
            if strong_patterns:
                pattern_names = [p.pattern_name.replace('_', ' ').title() for p in strong_patterns]
                reasoning_parts.append(f"Detected patterns: {', '.join(pattern_names)}")

    # Add style reasoning
    profile = st.session_state.personality_profiler.current_profile
    if profile:
        reasoning_parts.append(f"Adapting to {profile.primary_style.value} communication style")

    # For demo purposes, simulate an intelligent response
    # In production, this would call the actual LLM API
    response_templates = {
        'introduction': [
            f"Hello {user_input.split()[2] if len(user_input.split()) > 2 else 'friend'}! It's wonderful to meet someone drawn to discovering their spiritual gifts.",
            "I can already sense some beautiful themes emerging from what you've shared.",
            "Your heart for growth and discovery really comes through in your words."
        ],
        'skills_assessment': [
            "That's a beautiful insight about your natural abilities.",
            "I'm noticing some strong patterns in what you're sharing about your strengths.",
            "It sounds like you have some real gifts in this area."
        ],
        'passion_exploration': [
            "The passion in your voice really comes through when you talk about this.",
            "I can see how this energizes you - that's often a sign of spiritual gifting.",
            "What you're describing aligns beautifully with what you've shared about your skills."
        ]
    }

    templates = response_templates.get(st.session_state.current_stage, ["That's a meaningful insight."])
    base_response = templates[st.session_state.total_exchanges % len(templates)]

    # Adapt based on communication style
    if profile and profile.primary_style.value == 'expressive':
        base_response = base_response.replace("insight", "beautiful insight")
        base_response = f"{base_response} I can feel the enthusiasm in your words!"
    elif profile and profile.primary_style.value == 'analytical':
        base_response = f"{base_response} Let me build on that with a specific follow-up question."

    reasoning = " | ".join(reasoning_parts) if reasoning_parts else "Standard response generation"

    return base_response, reasoning

def force_new_question():
    """Force generation of a different type of question"""
    # This would implement alternative question generation
    st.info("Generated alternative question approach")

def show_detailed_insights():
    """Show comprehensive AI insights analysis"""
    if not st.session_state.show_insights:
        return

    st.header("🧠 Detailed AI Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Discovered Insights")
        if st.session_state.context_manager.insights:
            insights_df = pd.DataFrame([
                {
                    'Stage': insight.stage,
                    'Type': insight.insight_type.replace('_', ' ').title(),
                    'Confidence': f"{insight.confidence:.2f}",
                    'Content': insight.content[:100] + "..." if len(insight.content) > 100 else insight.content
                }
                for insight in st.session_state.context_manager.insights
            ])
            st.dataframe(insights_df, use_container_width=True)
        else:
            st.info("Continue the conversation to discover more insights!")

    with col2:
        st.subheader("📊 Theme Strength")
        if st.session_state.context_manager.themes:
            theme_data = [
                {'Theme': theme_name.title(), 'Strength': theme.strength}
                for theme_name, theme in st.session_state.context_manager.themes.items()
            ]

            df = pd.DataFrame(theme_data)
            fig = px.bar(df, x='Theme', y='Strength', title="Emerging Themes by Strength")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Themes will appear as patterns emerge in your responses.")

def show_personality_analysis():
    """Show detailed personality profile analysis"""
    if not st.session_state.show_personality:
        return

    st.header("🎭 Personality Analysis")

    profile = st.session_state.personality_profiler.current_profile
    if not profile:
        st.info("Keep responding to build your personality profile! (Need at least 3 responses)")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Communication Style")

        # Style radar chart
        markers = profile.markers

        style_data = {
            'Dimension': ['Word Count', 'Emotional Language', 'Enthusiasm', 'Certainty', 'Concrete Thinking'],
            'Score': [
                min(markers.word_count_avg / 50, 1.0),  # Normalize to 0-1
                markers.emotional_language_frequency * 20,  # Scale up
                markers.enthusiasm_markers * 10,  # Scale up
                1.0 - markers.uncertainty_indicators * 5,  # Invert uncertainty
                markers.concrete_vs_abstract_ratio
            ]
        }

        fig = go.Figure(data=go.Scatterpolar(
            r=style_data['Score'],
            theta=style_data['Dimension'],
            fill='toself',
            name=f'{profile.primary_style.value.title()} Style'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=False,
            title="Communication Pattern"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Style Characteristics")
        st.metric("Primary Style", profile.primary_style.value.title())
        st.metric("Confidence", f"{profile.confidence:.2f}")
        st.metric("Preferred Depth", profile.preferred_depth.value.title())

        st.subheader("Adaptations")
        for adaptation in profile.adaptations[:5]:
            st.write(f"• {adaptation}")

def export_session():
    """Export session data for user"""
    # Create export data
    export_data = {
        'session_info': {
            'start_time': st.session_state.session_start.isoformat(),
            'total_exchanges': st.session_state.total_exchanges,
            'current_stage': st.session_state.current_stage
        },
        'conversation_history': st.session_state.conversation_history,
        'insights': [
            {
                'content': insight.content,
                'confidence': insight.confidence,
                'type': insight.insight_type,
                'stage': insight.stage
            }
            for insight in st.session_state.context_manager.insights
        ] if hasattr(st.session_state, 'context_manager') else [],
        'themes': {
            name: {'strength': theme.strength, 'evidence_count': len(theme.evidence)}
            for name, theme in st.session_state.context_manager.themes.items()
        } if hasattr(st.session_state, 'context_manager') else {},
        'personality_profile': {
            'style': st.session_state.personality_profiler.current_profile.primary_style.value,
            'confidence': st.session_state.personality_profiler.current_profile.confidence,
            'adaptations': st.session_state.personality_profiler.current_profile.adaptations
        } if st.session_state.personality_profiler.current_profile else None
    }

    # Convert to JSON
    json_data = json.dumps(export_data, indent=2, default=str)

    # Offer download
    st.download_button(
        label="📄 Download Session Data",
        data=json_data,
        file_name=f"spiritual_gifts_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

    st.success("Session export ready! Click the button above to download.")

def main():
    """Main Streamlit application"""
    initialize_session_state()

    # Main layout
    create_sidebar()

    # Show insights if requested
    if st.session_state.show_insights:
        show_detailed_insights()
        if st.button("← Back to Conversation"):
            st.session_state.show_insights = False
            st.rerun()
        return

    # Show personality analysis if requested
    if st.session_state.show_personality:
        show_personality_analysis()
        if st.button("← Back to Conversation"):
            st.session_state.show_personality = False
            st.rerun()
        return

    # Show analytics dashboard if requested
    if st.session_state.show_analytics:
        render_visualization_dashboard(st.session_state)
        if st.button("← Back to Conversation"):
            st.session_state.show_analytics = False
            st.rerun()
        return

    # Show export options if requested
    if st.session_state.show_export:
        render_export_options(st.session_state)
        if st.button("← Back to Conversation"):
            st.session_state.show_export = False
            st.rerun()
        return

    # Main conversation interface
    create_conversation_interface()

    # Discovery completion
    if st.session_state.discovery_complete:
        st.success("🎉 Congratulations! You've completed your spiritual gifts discovery journey!")
        st.balloons()

        if st.button("📊 Generate Final Assessment"):
            # This would generate the complete assessment
            st.info("Final assessment generation would happen here using our Phase 3/4 systems")

if __name__ == "__main__":
    main()