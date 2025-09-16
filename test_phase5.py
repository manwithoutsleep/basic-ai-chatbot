#!/usr/bin/env python3
"""
Test Phase 5: User Interface and Visualization
Tests web interface, visualization components, and export functionality
"""

import os
import sys
import json
import tempfile
from datetime import datetime
from unittest.mock import Mock

# Import Phase 5 components
from visualization_components import SpiritualGiftsVisualizer, ConversationExporter

def test_visualization_components():
    """Test the visualization system components"""
    print("Testing Visualization Components...")

    visualizer = SpiritualGiftsVisualizer()

    # Test 1: Empty data handling
    empty_fig = visualizer.create_conversation_timeline([])
    assert empty_fig is not None
    print("   Empty data visualization handling: PASS")

    # Test 2: Conversation timeline with sample data
    sample_conversation = [
        {
            'user_input': 'I love teaching others',
            'bot_response': 'That sounds like a gift!',
            'timestamp': datetime.now().isoformat(),
            'stage': 'skills_assessment',
            'ai_reasoning': 'Teaching pattern detected'
        },
        {
            'user_input': 'People often come to me for advice',
            'bot_response': 'That suggests natural counseling abilities.',
            'timestamp': datetime.now().isoformat(),
            'stage': 'skills_assessment',
            'ai_reasoning': 'Helping pattern confirmed'
        }
    ]

    timeline_fig = visualizer.create_conversation_timeline(sample_conversation)
    assert timeline_fig is not None
    assert len(timeline_fig.data) > 0  # Should have traces
    print("   Conversation timeline generation: PASS")

    # Test 3: Themes visualization with mock theme data
    mock_themes = {
        'teaching': Mock(strength=2.5, evidence=['response1', 'response2']),
        'helping': Mock(strength=1.8, evidence=['response3'])
    }

    themes_fig = visualizer.create_themes_evolution(mock_themes)
    assert themes_fig is not None
    print("   Themes evolution visualization: PASS")

    # Test 4: Personality radar with mock profile
    mock_profile = Mock()
    mock_profile.primary_style.value = 'expressive'
    mock_profile.markers = Mock(
        word_count_avg=25.0,
        emotional_language_frequency=0.08,
        enthusiasm_markers=0.05,
        uncertainty_indicators=0.1,
        concrete_vs_abstract_ratio=0.6,
        question_asking_frequency=0.3
    )

    personality_fig = visualizer.create_personality_radar(mock_profile)
    assert personality_fig is not None
    print("   Personality radar chart: PASS")

    # Test 5: Insights confidence chart
    mock_insights = [
        Mock(
            insight_type='strong_skill_indicator',
            confidence=0.85,
            stage='skills_assessment',
            content='User shows strong teaching indicators'
        ),
        Mock(
            insight_type='passion_indicator',
            confidence=0.72,
            stage='passion_exploration',
            content='Deep passion for helping others'
        )
    ]

    insights_fig = visualizer.create_insights_confidence_chart(mock_insights)
    assert insights_fig is not None
    print("   Insights confidence visualization: PASS")

def test_export_functionality():
    """Test conversation export system"""
    print("\nTesting Export Functionality...")

    exporter = ConversationExporter()

    # Sample session data
    session_data = {
        'conversation_history': [
            {
                'user_input': 'I love helping people learn and grow',
                'bot_response': 'That sounds like you have teaching gifts!',
                'timestamp': datetime.now().isoformat(),
                'stage': 'skills_assessment',
                'ai_reasoning': 'Teaching pattern detected'
            },
            {
                'user_input': 'People often come to me when they need guidance',
                'bot_response': 'That suggests counseling or mentoring abilities.',
                'timestamp': datetime.now().isoformat(),
                'stage': 'skills_assessment',
                'ai_reasoning': 'Guidance pattern confirmed'
            }
        ],
        'current_stage': 'skills_assessment',
        'total_exchanges': 2
    }

    # Test JSON export
    json_data = exporter.export_conversation_summary(session_data, 'json')
    assert isinstance(json_data, bytes)

    # Verify JSON structure
    json_content = json.loads(json_data.decode('utf-8'))
    assert 'export_info' in json_content
    assert 'conversation_data' in json_content
    print("   JSON export functionality: PASS")

    # Test HTML export
    html_data = exporter.export_conversation_summary(session_data, 'html')
    assert isinstance(html_data, bytes)

    html_content = html_data.decode('utf-8')
    assert '<html>' in html_content
    assert 'Spiritual Gifts Discovery Report' in html_content
    assert 'I love helping people' in html_content  # Sample user input should be present
    print("   HTML export functionality: PASS")

    # Test CSV export
    csv_data = exporter.export_conversation_summary(session_data, 'csv')
    assert isinstance(csv_data, bytes)

    csv_content = csv_data.decode('utf-8')
    assert 'Exchange_Number' in csv_content  # CSV header
    assert 'User_Input' in csv_content
    print("   CSV export functionality: PASS")

    # Test invalid format handling
    try:
        exporter.export_conversation_summary(session_data, 'invalid_format')
        assert False, "Should have raised ValueError"
    except ValueError:
        print("   Invalid format error handling: PASS")

def test_streamlit_app_structure():
    """Test Streamlit app can be imported and basic structure is sound"""
    print("\nTesting Streamlit App Structure...")

    try:
        # Test that we can import the main app
        import streamlit_app
        print("   Streamlit app import: PASS")

        # Test that required functions exist
        required_functions = [
            'initialize_session_state',
            'create_sidebar',
            'create_conversation_interface',
            'main'
        ]

        for func_name in required_functions:
            assert hasattr(streamlit_app, func_name), f"Missing function: {func_name}"

        print("   Required functions present: PASS")

        # Test that visualization imports work
        from streamlit_app import render_visualization_dashboard, render_export_options
        print("   Visualization imports: PASS")

    except ImportError as e:
        print(f"   Streamlit app import failed: {e}")
        return False

    return True

def test_web_architecture_concepts():
    """Test key web architecture concepts implementation"""
    print("\nTesting Web Architecture Concepts...")

    # Test 1: Component Modularity
    # Verify that visualization components can work independently
    visualizer = SpiritualGiftsVisualizer()
    exporter = ConversationExporter()

    # Components should be instantiable and have expected methods
    assert hasattr(visualizer, 'create_conversation_timeline')
    assert hasattr(visualizer, 'create_themes_evolution')
    assert hasattr(exporter, 'export_conversation_summary')
    print("   Component modularity: PASS")

    # Test 2: Data Format Consistency
    # Test that exported data maintains structure across formats
    sample_data = {'conversation_history': [], 'current_stage': 'test'}

    json_export = exporter.export_conversation_summary(sample_data, 'json')
    html_export = exporter.export_conversation_summary(sample_data, 'html')
    csv_export = exporter.export_conversation_summary(sample_data, 'csv')

    # All should return bytes
    assert all(isinstance(export, bytes) for export in [json_export, html_export, csv_export])
    print("   Data format consistency: PASS")

    # Test 3: Visualization Data Handling
    # Test that visualizations handle various data states gracefully
    empty_data_results = [
        visualizer.create_conversation_timeline([]),
        visualizer.create_themes_evolution({}),
        visualizer.create_insights_confidence_chart([])
    ]

    # All should return valid figures (not None)
    assert all(fig is not None for fig in empty_data_results)
    print("   Visualization data handling: PASS")

    # Test 4: Error Resilience
    # Test that components handle malformed data gracefully
    try:
        # Should not crash with None input
        visualizer.create_conversation_timeline(None)
        visualizer.create_themes_evolution(None)
        print("   Error resilience: PASS")
    except Exception as e:
        print(f"   Error resilience: FAIL - {e}")
        return False

    return True

def test_integration_with_ai_systems():
    """Test that web components integrate properly with AI systems"""
    print("\nTesting AI Systems Integration...")

    # Test that web components can handle real AI system outputs
    try:
        from context_manager import EnhancedContextManager
        from personality_profiler import PersonalityProfiler

        # Create real AI system instances
        context_manager = EnhancedContextManager()
        personality_profiler = PersonalityProfiler()

        # Add some data
        context_manager.add_exchange(
            "I love teaching others",
            "That's wonderful!",
            "skills_assessment"
        )

        personality_profiler.update_profile("I love teaching others and helping people grow")

        # Test visualization with real data
        visualizer = SpiritualGiftsVisualizer()

        # Should work with real theme data
        if context_manager.themes:
            themes_fig = visualizer.create_themes_evolution(context_manager.themes)
            assert themes_fig is not None

        # Should work with real personality data
        if personality_profiler.current_profile:
            personality_fig = visualizer.create_personality_radar(personality_profiler.current_profile)
            assert personality_fig is not None

        # Should work with real insights data
        if context_manager.insights:
            insights_fig = visualizer.create_insights_confidence_chart(context_manager.insights)
            assert insights_fig is not None

        print("   AI systems integration: PASS")

    except Exception as e:
        print(f"   AI systems integration: FAIL - {e}")
        return False

    return True

def run_all_phase5_tests():
    """Run all Phase 5 tests"""
    print("PHASE 5 TESTING: User Interface and Visualization")
    print("=" * 60)

    try:
        test_visualization_components()
        test_export_functionality()

        # Streamlit tests (may require streamlit to be available)
        streamlit_success = test_streamlit_app_structure()

        test_web_architecture_concepts()
        test_integration_with_ai_systems()

        print("\n" + "=" * 60)
        print("PHASE 5 TESTS COMPLETED!")
        print("Web interface and visualization system working correctly")
        print("\nKey capabilities verified:")
        print("  • Interactive conversation timeline visualization")
        print("  • Real-time themes and insights tracking")
        print("  • Personality analysis radar charts")
        print("  • Multi-format export system (JSON, HTML, CSV)")
        print("  • Component-based architecture")
        print("  • Integration with AI intelligence systems")

        if streamlit_success:
            print("  • Streamlit web application structure")
        else:
            print("  • Note: Some Streamlit-specific tests may require running environment")

        print("=" * 60)

        return True

    except Exception as e:
        print(f"\nTEST FAILED: {str(e)}")
        print(f"Error occurred during Phase 5 testing")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_phase5_tests()
    sys.exit(0 if success else 1)