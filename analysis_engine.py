#!/usr/bin/env python3
"""
Skills vs. Passions Analysis Engine
Analyzes user responses to identify patterns and overlaps between skills and passions
"""

import re
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set

class SkillsPassionsAnalyzer:
    """Analyzes user responses to find patterns between skills and passions"""

    def __init__(self):
        # Keyword mappings for different categories
        self.skill_keywords = {
            'teaching': ['teach', 'mentor', 'guide', 'explain', 'instruct', 'train', 'educate', 'coach'],
            'leadership': ['lead', 'manage', 'organize', 'coordinate', 'direct', 'supervise', 'delegate'],
            'communication': ['speak', 'write', 'present', 'communicate', 'express', 'articulate', 'convey'],
            'helping': ['help', 'assist', 'support', 'serve', 'care', 'counsel', 'encourage', 'comfort'],
            'creative': ['create', 'design', 'artistic', 'creative', 'imagine', 'innovate', 'craft', 'build'],
            'analytical': ['analyze', 'research', 'investigate', 'study', 'examine', 'solve', 'logical'],
            'administrative': ['organize', 'plan', 'schedule', 'coordinate', 'detail', 'systematic'],
            'technical': ['technical', 'technology', 'programming', 'engineering', 'computing', 'digital']
        }

        self.passion_keywords = {
            'people': ['people', 'relationships', 'community', 'social', 'family', 'friends', 'connection'],
            'justice': ['justice', 'fair', 'equality', 'rights', 'advocacy', 'change', 'reform'],
            'nature': ['nature', 'environment', 'outdoors', 'animals', 'earth', 'conservation'],
            'creativity': ['art', 'music', 'creative', 'beauty', 'expression', 'imagination', 'design'],
            'learning': ['learn', 'knowledge', 'education', 'study', 'growth', 'discovery', 'wisdom'],
            'service': ['serve', 'volunteer', 'giving', 'ministry', 'mission', 'charity', 'helping'],
            'innovation': ['innovation', 'technology', 'progress', 'future', 'advancement', 'improvement'],
            'healing': ['health', 'healing', 'wellness', 'medical', 'therapy', 'recovery', 'wholeness']
        }

        self.spiritual_gift_indicators = {
            'teaching': {
                'skills': ['teaching', 'communication', 'analytical'],
                'passions': ['learning', 'people'],
                'description': 'The ability to understand and communicate truth in ways that help others learn and grow'
            },
            'leadership': {
                'skills': ['leadership', 'communication', 'administrative'],
                'passions': ['people', 'service', 'justice'],
                'description': 'The ability to inspire and guide others toward common goals and positive change'
            },
            'helping': {
                'skills': ['helping', 'communication'],
                'passions': ['people', 'service', 'healing'],
                'description': 'The gift of coming alongside others to provide practical assistance and emotional support'
            },
            'mercy': {
                'skills': ['helping', 'communication'],
                'passions': ['people', 'healing', 'justice'],
                'description': 'Deep compassion that moves you to action when you see others suffering'
            },
            'administration': {
                'skills': ['administrative', 'leadership', 'analytical'],
                'passions': ['service', 'people'],
                'description': 'The ability to organize resources and coordinate efforts to accomplish important goals'
            },
            'creativity': {
                'skills': ['creative', 'communication'],
                'passions': ['creativity', 'people', 'service'],
                'description': 'Using artistic expression to inspire, heal, and bring beauty into the world'
            },
            'prophecy': {
                'skills': ['communication', 'analytical'],
                'passions': ['justice', 'people'],
                'description': 'The ability to see truth clearly and speak it boldly for positive change'
            },
            'evangelism': {
                'skills': ['communication', 'helping'],
                'passions': ['people', 'service'],
                'description': 'Natural ability to share good news and connect people with hope and purpose'
            }
        }

    def extract_themes(self, responses: List[str]) -> Dict[str, int]:
        """Extract themes from a list of response strings"""
        themes = defaultdict(int)

        for response in responses:
            response_lower = response.lower()

            # Check skill keywords
            for skill_category, keywords in self.skill_keywords.items():
                for keyword in keywords:
                    if keyword in response_lower:
                        themes[f"skill_{skill_category}"] += 1

            # Check passion keywords
            for passion_category, keywords in self.passion_keywords.items():
                for keyword in keywords:
                    if keyword in response_lower:
                        themes[f"passion_{passion_category}"] += 1

        return dict(themes)

    def analyze_skills(self, skills_responses: List[Dict]) -> Dict:
        """Analyze skills assessment responses"""
        if not skills_responses:
            return {}

        response_texts = [r.get('response', '') for r in skills_responses]
        themes = self.extract_themes(response_texts)

        # Filter to skill themes only
        skill_themes = {k.replace('skill_', ''): v for k, v in themes.items() if k.startswith('skill_')}

        # Find top skills
        top_skills = sorted(skill_themes.items(), key=lambda x: x[1], reverse=True)[:3]

        return {
            'raw_responses': response_texts,
            'themes': skill_themes,
            'top_skills': [skill for skill, _ in top_skills],
            'skill_scores': dict(top_skills)
        }

    def analyze_passions(self, passion_responses: List[Dict]) -> Dict:
        """Analyze passion exploration responses"""
        if not passion_responses:
            return {}

        response_texts = [r.get('response', '') for r in passion_responses]
        themes = self.extract_themes(response_texts)

        # Filter to passion themes only
        passion_themes = {k.replace('passion_', ''): v for k, v in themes.items() if k.startswith('passion_')}

        # Find top passions
        top_passions = sorted(passion_themes.items(), key=lambda x: x[1], reverse=True)[:3]

        return {
            'raw_responses': response_texts,
            'themes': passion_themes,
            'top_passions': [passion for passion, _ in top_passions],
            'passion_scores': dict(top_passions)
        }

    def find_skill_passion_overlaps(self, skills_analysis: Dict, passions_analysis: Dict) -> List[Tuple[str, str, str]]:
        """Find areas where skills and passions align"""
        overlaps = []

        if not skills_analysis or not passions_analysis:
            return overlaps

        skills = skills_analysis.get('top_skills', [])
        passions = passions_analysis.get('top_passions', [])

        # Direct matches (same word/concept)
        direct_matches = set(skills) & set(passions)
        for match in direct_matches:
            overlaps.append((match, match, "direct_match"))

        # Conceptual overlaps based on spiritual gift patterns
        for gift, indicators in self.spiritual_gift_indicators.items():
            skill_matches = len(set(skills) & set(indicators['skills']))
            passion_matches = len(set(passions) & set(indicators['passions']))

            # If we have matches in both skills and passions for this gift
            if skill_matches > 0 and passion_matches > 0:
                matching_skills = list(set(skills) & set(indicators['skills']))
                matching_passions = list(set(passions) & set(indicators['passions']))

                for skill in matching_skills:
                    for passion in matching_passions:
                        overlaps.append((skill, passion, gift))

        return overlaps

    def calculate_alignment_score(self, skills_analysis: Dict, passions_analysis: Dict) -> float:
        """Calculate a numerical score for skills-passions alignment"""
        if not skills_analysis or not passions_analysis:
            return 0.0

        overlaps = self.find_skill_passion_overlaps(skills_analysis, passions_analysis)

        # Base score from number of overlaps
        overlap_score = min(len(overlaps) * 20, 60)  # Max 60 points from overlaps

        # Bonus for spiritual gift alignment
        gift_alignments = [overlap for overlap in overlaps if overlap[2] in self.spiritual_gift_indicators]
        gift_score = min(len(set(overlap[2] for overlap in gift_alignments)) * 10, 40)  # Max 40 points

        return min(overlap_score + gift_score, 100)

    def identify_potential_spiritual_gifts(self, skills_analysis: Dict, passions_analysis: Dict) -> List[Dict]:
        """Identify potential spiritual gifts based on skills and passions"""
        potential_gifts = []

        if not skills_analysis or not passions_analysis:
            return potential_gifts

        skills = skills_analysis.get('top_skills', [])
        passions = passions_analysis.get('top_passions', [])

        for gift_name, indicators in self.spiritual_gift_indicators.items():
            skill_matches = set(skills) & set(indicators['skills'])
            passion_matches = set(passions) & set(indicators['passions'])

            # Calculate strength score
            skill_score = len(skill_matches) / len(indicators['skills'])
            passion_score = len(passion_matches) / len(indicators['passions'])
            total_score = (skill_score + passion_score) / 2

            if total_score > 0:  # Any alignment
                potential_gifts.append({
                    'name': gift_name,
                    'score': total_score,
                    'description': indicators['description'],
                    'matching_skills': list(skill_matches),
                    'matching_passions': list(passion_matches),
                    'strength': self._categorize_strength(total_score)
                })

        # Sort by score
        potential_gifts.sort(key=lambda x: x['score'], reverse=True)
        return potential_gifts

    def _categorize_strength(self, score: float) -> str:
        """Categorize gift strength based on score"""
        if score >= 0.7:
            return "Strong"
        elif score >= 0.4:
            return "Moderate"
        elif score >= 0.2:
            return "Emerging"
        else:
            return "Potential"

    def generate_analysis_summary(self, user_responses: Dict) -> Dict:
        """Generate comprehensive analysis of user's discovery session"""

        # Analyze skills and passions
        skills_analysis = self.analyze_skills(user_responses.get('skills_assessment', []))
        passions_analysis = self.analyze_passions(user_responses.get('passion_exploration', []))

        # Find overlaps and alignment
        overlaps = self.find_skill_passion_overlaps(skills_analysis, passions_analysis)
        alignment_score = self.calculate_alignment_score(skills_analysis, passions_analysis)
        potential_gifts = self.identify_potential_spiritual_gifts(skills_analysis, passions_analysis)

        # Extract values insights
        values_responses = user_responses.get('values_clarification', [])
        values_text = ' '.join([r.get('response', '') for r in values_responses])

        return {
            'skills_analysis': skills_analysis,
            'passions_analysis': passions_analysis,
            'skill_passion_overlaps': overlaps,
            'alignment_score': alignment_score,
            'potential_spiritual_gifts': potential_gifts[:5],  # Top 5
            'values_insights': values_text,
            'analysis_timestamp': __import__('datetime').datetime.now().isoformat(),
            'summary': self._generate_text_summary(skills_analysis, passions_analysis, overlaps, potential_gifts)
        }

    def _generate_text_summary(self, skills_analysis: Dict, passions_analysis: Dict,
                              overlaps: List, potential_gifts: List[Dict]) -> str:
        """Generate a human-readable summary"""
        summary_parts = []

        # Skills summary
        if skills_analysis and skills_analysis.get('top_skills'):
            skills_text = ', '.join(skills_analysis['top_skills'])
            summary_parts.append(f"Your strongest skills appear to be: {skills_text}")

        # Passions summary
        if passions_analysis and passions_analysis.get('top_passions'):
            passions_text = ', '.join(passions_analysis['top_passions'])
            summary_parts.append(f"Your core passions center around: {passions_text}")

        # Overlaps
        if overlaps:
            unique_overlaps = list(set(overlap[2] for overlap in overlaps if overlap[2] != "direct_match"))
            if unique_overlaps:
                summary_parts.append(f"Areas of alignment point toward: {', '.join(unique_overlaps)}")

        # Top spiritual gifts
        if potential_gifts:
            top_gift = potential_gifts[0]
            summary_parts.append(f"Your strongest spiritual gift indicator is {top_gift['name']} ({top_gift['strength']} strength)")

        return '. '.join(summary_parts) + '.'


if __name__ == "__main__":
    # Test the analyzer with sample data
    analyzer = SkillsPassionsAnalyzer()

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
        ]
    }

    analysis = analyzer.generate_analysis_summary(sample_responses)
    print("Sample Analysis Results:")
    print(f"Alignment Score: {analysis['alignment_score']}")
    print(f"Summary: {analysis['summary']}")
    print("\nPotential Gifts:")
    for gift in analysis['potential_spiritual_gifts']:
        print(f"- {gift['name']} ({gift['strength']}): {gift['description']}")