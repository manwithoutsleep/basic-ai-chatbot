#!/usr/bin/env python3
"""
Test Phase 3: Self-Discovery Logic Engine
Tests all components of the spiritual gifts discovery system
"""

import os
import sys
import json
from datetime import datetime

# Import our Phase 3 components
from discovery_engine import DiscoverySession
from analysis_engine import SkillsPassionsAnalyzer
from scoring_system import SpiritualGiftsAssessment

def test_discovery_session():
    """Test the discovery session progression system"""
    print("Testing Discovery Session...")

    session = DiscoverySession()

    # Test initial state
    assert session.get_current_stage() == "introduction"
    assert session.current_stage == 0

    # Test getting questions
    first_question = session.get_next_question()
    assert first_question is not None
    assert "Hello" in first_question or "name" in first_question

    # Test processing responses
    test_response = "My name is Alex and I'm excited to discover my gifts"
    success = session.process_response(test_response)
    assert success == True

    # Test that response was stored
    intro_responses = session.user_responses["introduction"]
    assert len(intro_responses) == 1
    assert intro_responses[0]["response"] == test_response

    # Test stage progression through multiple responses
    for stage in session.stages:
        questions = session.get_stage_questions(stage)
        for i, question in enumerate(questions):
            if session.get_current_stage() == stage:
                test_resp = f"Test response for {stage} question {i+1}"
                session.process_response(test_resp)

    # Verify session completion
    final_question = session.get_next_question()
    current_stage = session.get_current_stage()

    print(f"   Session progressed through all stages")
    print(f"   Final stage: {current_stage}")
    print(f"   Total responses: {sum(len(r) for r in session.user_responses.values())}")

def test_skills_passions_analyzer():
    """Test the analysis engine"""
    print("\nTesting Skills & Passions Analyzer...")

    analyzer = SkillsPassionsAnalyzer()

    # Test data
    sample_responses = {
        'skills_assessment': [
            {'response': 'I love teaching others and helping them understand complex concepts'},
            {'response': 'People often come to me for advice and guidance'},
            {'response': 'I excel at organizing events and managing projects'}
        ],
        'passion_exploration': [
            {'response': 'I feel most alive when helping people grow and learn'},
            {'response': 'Education and human development really stir my heart'},
            {'response': 'I care deeply about justice and equality in our communities'}
        ],
        'values_clarification': [
            {'response': 'Truth and growth are extremely important to me'},
            {'response': 'I believe in the potential of every person'}
        ]
    }

    # Test skills analysis
    skills_analysis = analyzer.analyze_skills(sample_responses['skills_assessment'])
    assert 'top_skills' in skills_analysis
    assert len(skills_analysis['top_skills']) > 0

    # Test passions analysis
    passions_analysis = analyzer.analyze_passions(sample_responses['passion_exploration'])
    assert 'top_passions' in passions_analysis
    assert len(passions_analysis['top_passions']) > 0

    # Test overlap detection
    overlaps = analyzer.find_skill_passion_overlaps(skills_analysis, passions_analysis)
    assert isinstance(overlaps, list)

    # Test alignment scoring
    alignment_score = analyzer.calculate_alignment_score(skills_analysis, passions_analysis)
    assert 0 <= alignment_score <= 100

    # Test comprehensive analysis
    full_analysis = analyzer.generate_analysis_summary(sample_responses)
    assert 'skills_analysis' in full_analysis
    assert 'passions_analysis' in full_analysis
    assert 'alignment_score' in full_analysis

    print(f"   Skills identified: {skills_analysis['top_skills']}")
    print(f"   Passions identified: {passions_analysis['top_passions']}")
    print(f"   Alignment score: {alignment_score}")
    print(f"   Overlaps found: {len(overlaps)}")

def test_scoring_system():
    """Test the spiritual gifts assessment system"""
    print("\nTesting Scoring System...")

    assessor = SpiritualGiftsAssessment()

    # Test data with strong teaching indicators
    sample_responses = {
        'introduction': [
            {'response': 'I am Sarah and I love helping people discover their potential'}
        ],
        'skills_assessment': [
            {'response': 'I love teaching others and helping them understand complex concepts'},
            {'response': 'People often come to me for advice and guidance'},
            {'response': 'I excel at organizing events and managing projects'},
            {'response': 'I naturally explain things in ways others can understand'}
        ],
        'passion_exploration': [
            {'response': 'I feel most alive when helping people grow and learn'},
            {'response': 'Education and human development really stir my heart'},
            {'response': 'I care deeply about justice and equality in our communities'},
            {'response': 'Seeing others have breakthrough moments energizes me'}
        ],
        'values_clarification': [
            {'response': 'Truth and growth are extremely important to me'},
            {'response': 'I believe in the potential of every person'},
            {'response': 'Education and understanding drive most of my decisions'},
            {'response': 'I value wisdom and the sharing of knowledge'}
        ]
    }

    # Test gift scoring
    gift_scores = assessor.calculate_gift_scores(sample_responses)
    assert isinstance(gift_scores, dict)
    assert len(gift_scores) > 0

    # Check that teaching should score highly with this data
    teaching_score = gift_scores.get('teaching', {}).get('total_score', 0)
    assert teaching_score > 30  # Should have moderate to strong teaching indicators

    # Test comprehensive assessment
    assessment = assessor.generate_comprehensive_assessment(sample_responses)
    assert 'top_gifts' in assessment
    assert 'readiness_score' in assessment
    assert 'recommendations' in assessment
    assert len(assessment['top_gifts']) <= 3

    top_gift = assessment['top_gifts'][0] if assessment['top_gifts'] else None

    print(f"   Gift scores calculated for {len(gift_scores)} gifts")
    if top_gift:
        print(f"   Top gift: {top_gift['name']} ({top_gift['score']}% - {top_gift['strength']})")
    print(f"   Readiness score: {assessment['readiness_score']}")
    print(f"   Recommendations: {len(assessment['recommendations'])}")

def test_integration():
    """Test that all components work together"""
    print("\nTesting Full Integration...")

    # Create a complete discovery session with realistic data
    session = DiscoverySession()

    # Simulate a complete discovery journey
    stages_data = {
        'introduction': [
            "Hi, I'm Maria. I'm exploring my calling because I want to make a meaningful impact",
            "I find joy in seeing others succeed and reach their potential",
            "I've taken some assessments before but want to go deeper"
        ],
        'skills_assessment': [
            "I'm naturally good at explaining complex things in simple ways",
            "People say I'm a good listener and give helpful advice",
            "I'm organized and good at planning events and projects",
            "I seem to motivate others and help them see possibilities"
        ],
        'passion_exploration': [
            "I lose track of time when I'm mentoring someone or teaching",
            "I dream about starting programs that help people grow",
            "Social justice and equality really stir my heart deeply",
            "I feel most alive when I see someone have a breakthrough"
        ],
        'values_clarification': [
            "Growth and learning guide most of my important decisions",
            "I want to be remembered for helping others discover their gifts",
            "Injustice motivates me to take action and create change",
            "Making a difference means empowering others to flourish"
        ]
    }

    # Populate the session with responses
    for stage_name, responses in stages_data.items():
        stage_index = session.stages.index(stage_name)
        session.current_stage = stage_index

        for response in responses:
            session.process_response(response)

    # Run analysis
    analyzer = SkillsPassionsAnalyzer()
    analysis = analyzer.generate_analysis_summary(session.user_responses)

    # Run assessment
    assessor = SpiritualGiftsAssessment()
    assessment = assessor.generate_comprehensive_assessment(session.user_responses)

    # Verify integration works
    assert assessment['readiness_score'] > 0
    assert len(assessment['top_gifts']) > 0
    assert analysis['alignment_score'] > 0

    # Save test files
    session_filename = session.save_session("test_session.json")
    assessment_filename = assessor.save_assessment(assessment, "test_assessment.json")

    print(f"   Complete journey simulation successful")
    print(f"   Analysis alignment score: {analysis['alignment_score']}")
    print(f"   Assessment readiness score: {assessment['readiness_score']}")
    print(f"   Top identified gift: {assessment['top_gifts'][0]['name']}")
    print(f"   Session saved to: {session_filename}")
    print(f"   Assessment saved to: {assessment_filename}")

def run_all_tests():
    """Run all Phase 3 tests"""
    print("PHASE 3 TESTING: Self-Discovery Logic Engine")
    print("=" * 60)

    try:
        test_discovery_session()
        test_skills_passions_analyzer()
        test_scoring_system()
        test_integration()

        print("\n" + "=" * 60)
        print("ALL PHASE 3 TESTS PASSED!")
        print("Self-Discovery Logic Engine is working correctly")
        print("Ready for Phase 4: Enhanced Intelligence")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\nTEST FAILED: {str(e)}")
        print(f"Error occurred during testing")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)