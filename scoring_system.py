#!/usr/bin/env python3
"""
Scoring and Assessment System
Provides numerical scoring and assessment logic for spiritual gifts discovery
"""

import json
from typing import Dict, List, Tuple
from datetime import datetime
from analysis_engine import SkillsPassionsAnalyzer

class SpiritualGiftsAssessment:
    """Comprehensive scoring system for spiritual gifts assessment"""

    def __init__(self):
        self.analyzer = SkillsPassionsAnalyzer()

        # Detailed spiritual gifts framework with scoring criteria
        self.gifts_framework = {
            'teaching': {
                'description': 'The ability to understand and communicate truth effectively',
                'key_indicators': {
                    'skills': ['teaching', 'communication', 'analytical'],
                    'passions': ['learning', 'people'],
                    'values': ['truth', 'growth', 'education', 'understanding']
                },
                'behavioral_markers': [
                    'Others seek you out for explanations',
                    'You enjoy breaking down complex concepts',
                    'You feel satisfied when others understand',
                    'You naturally use examples and illustrations'
                ],
                'typical_expressions': [
                    'Formal teaching or training',
                    'Mentoring and coaching',
                    'Writing instructional content',
                    'Creating educational resources'
                ]
            },

            'leadership': {
                'description': 'The ability to inspire and guide others toward goals',
                'key_indicators': {
                    'skills': ['leadership', 'communication', 'administrative'],
                    'passions': ['people', 'service', 'justice'],
                    'values': ['vision', 'purpose', 'teamwork', 'progress']
                },
                'behavioral_markers': [
                    'People naturally follow your direction',
                    'You see the big picture and future possibilities',
                    'You motivate others to achieve more',
                    'You take initiative in group situations'
                ],
                'typical_expressions': [
                    'Team or organization leadership',
                    'Project management',
                    'Community organizing',
                    'Visionary planning'
                ]
            },

            'mercy': {
                'description': 'Deep compassion that moves you to help those who suffer',
                'key_indicators': {
                    'skills': ['helping', 'communication'],
                    'passions': ['people', 'healing', 'justice'],
                    'values': ['compassion', 'kindness', 'healing', 'restoration']
                },
                'behavioral_markers': [
                    'You are deeply moved by others suffering',
                    'You offer comfort naturally',
                    'You attract people who need encouragement',
                    'You see good in difficult people'
                ],
                'typical_expressions': [
                    'Counseling and support',
                    'Healthcare and healing',
                    'Working with marginalized people',
                    'Crisis intervention'
                ]
            },

            'administration': {
                'description': 'The ability to organize and coordinate for effective ministry',
                'key_indicators': {
                    'skills': ['administrative', 'leadership', 'analytical'],
                    'passions': ['service', 'people'],
                    'values': ['order', 'efficiency', 'stewardship', 'service']
                },
                'behavioral_markers': [
                    'You naturally organize and systematize',
                    'You see what needs to be done logistically',
                    'You coordinate resources effectively',
                    'You help others be more productive'
                ],
                'typical_expressions': [
                    'Event planning and coordination',
                    'Business and operations management',
                    'Resource allocation',
                    'Systems development'
                ]
            },

            'serving': {
                'description': 'Joy in meeting practical needs and supporting others',
                'key_indicators': {
                    'skills': ['helping', 'administrative'],
                    'passions': ['service', 'people'],
                    'values': ['service', 'humility', 'helpfulness', 'support']
                },
                'behavioral_markers': [
                    'You prefer to work behind the scenes',
                    'You notice practical needs others miss',
                    'You find joy in helping tasks get done',
                    'You work well under others leadership'
                ],
                'typical_expressions': [
                    'Volunteer coordination',
                    'Hospitality and events',
                    'Maintenance and support',
                    'Administrative assistance'
                ]
            },

            'encouraging': {
                'description': 'The ability to motivate and build up others',
                'key_indicators': {
                    'skills': ['communication', 'helping'],
                    'passions': ['people', 'healing'],
                    'values': ['hope', 'growth', 'potential', 'encouragement']
                },
                'behavioral_markers': [
                    'You see potential in others',
                    'You naturally motivate and inspire',
                    'People feel better after talking with you',
                    'You focus on solutions and possibilities'
                ],
                'typical_expressions': [
                    'Life coaching and mentoring',
                    'Motivational speaking',
                    'Counseling and therapy',
                    'Team building and development'
                ]
            },

            'giving': {
                'description': 'Joy in sharing resources generously for kingdom purposes',
                'key_indicators': {
                    'skills': ['administrative', 'analytical'],
                    'passions': ['service', 'justice'],
                    'values': ['generosity', 'stewardship', 'impact', 'justice']
                },
                'behavioral_markers': [
                    'You give quietly and consistently',
                    'You research where gifts will have most impact',
                    'You motivate others to give',
                    'You see resources as tools for good'
                ],
                'typical_expressions': [
                    'Philanthropy and donations',
                    'Fundraising and development',
                    'Financial planning for ministry',
                    'Resource mobilization'
                ]
            },

            'creativity': {
                'description': 'Using artistic gifts to inspire and communicate truth',
                'key_indicators': {
                    'skills': ['creative', 'communication'],
                    'passions': ['creativity', 'people', 'service'],
                    'values': ['beauty', 'expression', 'inspiration', 'truth']
                },
                'behavioral_markers': [
                    'You express yourself through artistic means',
                    'You use creativity to communicate deeper truths',
                    'You inspire others through your art',
                    'You see beauty and meaning in everyday things'
                ],
                'typical_expressions': [
                    'Visual and performing arts',
                    'Creative writing and storytelling',
                    'Design and aesthetics',
                    'Worship and celebration arts'
                ]
            }
        }

    def calculate_gift_scores(self, user_responses: Dict) -> Dict[str, Dict]:
        """Calculate detailed scores for each spiritual gift"""
        gift_scores = {}

        # Get analysis from the analyzer
        analysis = self.analyzer.generate_analysis_summary(user_responses)
        skills_analysis = analysis.get('skills_analysis', {})
        passions_analysis = analysis.get('passions_analysis', {})

        for gift_name, gift_info in self.gifts_framework.items():
            score_data = self._calculate_individual_gift_score(
                gift_name, gift_info, skills_analysis, passions_analysis, user_responses
            )
            gift_scores[gift_name] = score_data

        return gift_scores

    def _calculate_individual_gift_score(self, gift_name: str, gift_info: Dict,
                                       skills_analysis: Dict, passions_analysis: Dict,
                                       user_responses: Dict) -> Dict:
        """Calculate score for a single spiritual gift"""

        score_components = {
            'skills_alignment': 0,
            'passions_alignment': 0,
            'values_alignment': 0,
            'response_content': 0
        }

        # Skills alignment (25% of total score)
        user_skills = set(skills_analysis.get('top_skills', []))
        required_skills = set(gift_info['key_indicators']['skills'])
        if user_skills and required_skills:
            skills_overlap = len(user_skills & required_skills) / len(required_skills)
            score_components['skills_alignment'] = skills_overlap * 25

        # Passions alignment (25% of total score)
        user_passions = set(passions_analysis.get('top_passions', []))
        required_passions = set(gift_info['key_indicators']['passions'])
        if user_passions and required_passions:
            passions_overlap = len(user_passions & required_passions) / len(required_passions)
            score_components['passions_alignment'] = passions_overlap * 25

        # Values alignment (25% of total score)
        values_responses = user_responses.get('values_clarification', [])
        values_text = ' '.join([r.get('response', '').lower() for r in values_responses])
        required_values = gift_info['key_indicators']['values']

        values_matches = sum(1 for value in required_values if value in values_text)
        if required_values:
            values_score = (values_matches / len(required_values)) * 25
            score_components['values_alignment'] = values_score

        # Response content analysis (25% of total score)
        all_responses_text = ' '.join([
            r.get('response', '').lower()
            for stage_responses in user_responses.values()
            for r in stage_responses
        ])

        behavioral_matches = sum(
            1 for marker in gift_info['behavioral_markers']
            if any(keyword in all_responses_text for keyword in marker.lower().split())
        )

        if gift_info['behavioral_markers']:
            content_score = (behavioral_matches / len(gift_info['behavioral_markers'])) * 25
            score_components['response_content'] = content_score

        # Calculate total score
        total_score = sum(score_components.values())

        # Determine strength category
        strength = self._categorize_gift_strength(total_score)

        return {
            'total_score': round(total_score, 1),
            'score_components': score_components,
            'strength': strength,
            'description': gift_info['description'],
            'key_indicators': gift_info['key_indicators'],
            'typical_expressions': gift_info['typical_expressions']
        }

    def _categorize_gift_strength(self, score: float) -> str:
        """Categorize gift strength based on total score"""
        if score >= 70:
            return "Dominant"
        elif score >= 50:
            return "Strong"
        elif score >= 30:
            return "Moderate"
        elif score >= 15:
            return "Emerging"
        else:
            return "Low"

    def generate_comprehensive_assessment(self, user_responses: Dict) -> Dict:
        """Generate a complete spiritual gifts assessment"""

        # Calculate all gift scores
        gift_scores = self.calculate_gift_scores(user_responses)

        # Sort gifts by score
        sorted_gifts = sorted(
            gift_scores.items(),
            key=lambda x: x[1]['total_score'],
            reverse=True
        )

        # Identify top gifts
        top_gifts = sorted_gifts[:3]
        dominant_gifts = [
            (name, data) for name, data in sorted_gifts
            if data['strength'] in ['Dominant', 'Strong']
        ]

        # Calculate overall readiness score
        top_scores = [data['total_score'] for _, data in top_gifts]
        readiness_score = sum(top_scores) / len(top_scores) if top_scores else 0

        # Generate recommendations
        recommendations = self._generate_recommendations(top_gifts, readiness_score)

        # Create assessment summary
        assessment = {
            'assessment_id': f"assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'user_responses_summary': self._summarize_user_responses(user_responses),
            'gift_scores': gift_scores,
            'top_gifts': [
                {
                    'name': name,
                    'score': data['total_score'],
                    'strength': data['strength'],
                    'description': data['description']
                }
                for name, data in top_gifts
            ],
            'dominant_gifts': [
                {
                    'name': name,
                    'score': data['total_score'],
                    'strength': data['strength']
                }
                for name, data in dominant_gifts
            ],
            'readiness_score': round(readiness_score, 1),
            'recommendations': recommendations,
            'next_steps': self._generate_next_steps(top_gifts),
            'detailed_analysis': self.analyzer.generate_analysis_summary(user_responses)
        }

        return assessment

    def _summarize_user_responses(self, user_responses: Dict) -> Dict:
        """Create a summary of user responses for the assessment"""
        summary = {}

        for stage, responses in user_responses.items():
            if responses:
                summary[stage] = {
                    'response_count': len(responses),
                    'sample_response': responses[0].get('response', '') if responses else ''
                }

        return summary

    def _generate_recommendations(self, top_gifts: List[Tuple], readiness_score: float) -> List[str]:
        """Generate personalized recommendations based on assessment"""
        recommendations = []

        if readiness_score >= 60:
            recommendations.append("You show strong clarity in your spiritual gifts! Consider seeking opportunities to use these gifts more actively.")

        if readiness_score >= 40:
            recommendations.append("You have good awareness of your gifts. Focus on developing your top 1-2 gifts through practice and mentorship.")
        else:
            recommendations.append("Continue exploring your gifts through various experiences and feedback from others.")

        # Gift-specific recommendations
        for gift_name, gift_data in top_gifts:
            if gift_data['strength'] in ['Dominant', 'Strong']:
                expressions = gift_data['typical_expressions']
                recommendations.append(f"For your {gift_name} gift, consider: {expressions[0].lower()}")

        return recommendations

    def _generate_next_steps(self, top_gifts: List[Tuple]) -> List[str]:
        """Generate specific next steps for gift development"""
        next_steps = []

        if top_gifts:
            primary_gift = top_gifts[0]
            gift_name = primary_gift[0]
            next_steps.append(f"Find a mentor who demonstrates the {gift_name} gift well")
            next_steps.append(f"Look for opportunities to practice {gift_name} in low-risk environments")
            next_steps.append("Seek feedback from trusted friends about how they see these gifts in you")

        next_steps.append("Keep a journal of when you feel most energized and effective")
        next_steps.append("Continue learning about spiritual gifts through books, assessments, or courses")

        return next_steps

    def save_assessment(self, assessment: Dict, filename: str = None) -> str:
        """Save assessment results to file"""
        if not filename:
            assessment_id = assessment.get('assessment_id', 'assessment')
            filename = f"assessments/{assessment_id}.json"

        import os
        os.makedirs("assessments", exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(assessment, f, indent=2, ensure_ascii=False)

        return filename


if __name__ == "__main__":
    # Test the scoring system
    scorer = SpiritualGiftsAssessment()

    # Sample test data
    sample_responses = {
        'introduction': [
            {'response': 'I am Sarah and I love helping people discover their potential'}
        ],
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
            {'response': 'I believe in the potential of every person'},
            {'response': 'Education and understanding drive most of my decisions'}
        ]
    }

    assessment = scorer.generate_comprehensive_assessment(sample_responses)

    print("=== SPIRITUAL GIFTS ASSESSMENT RESULTS ===")
    print(f"Readiness Score: {assessment['readiness_score']}/100")
    print("\nTop 3 Gifts:")
    for i, gift in enumerate(assessment['top_gifts'], 1):
        print(f"{i}. {gift['name'].title()} - {gift['score']}% ({gift['strength']})")
        print(f"   {gift['description']}")

    print(f"\nRecommendations:")
    for rec in assessment['recommendations']:
        print(f"• {rec}")

    filename = scorer.save_assessment(assessment)
    print(f"\nAssessment saved to: {filename}")