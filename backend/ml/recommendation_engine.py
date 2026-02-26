"""
Career Recommendation Engine - Similarity-Based Matching

Replaces the RandomForest classification approach with a scalable,
explainable feature-vector similarity matching system.

This module provides:
  1. CareerDatabase: Load and manage career feature vectors
  2. UserFeatureExtractor: Convert quiz answers to feature vectors
  3. RecommendationEngine: Similarity-based ranking
  4. ExplanationGenerator: Human-readable justified recommendations
"""

import json
import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Career:
    """Represents a career with its feature vector."""
    id: str
    name: str
    description: str
    features: Dict[str, float]
    salary_range: str = "Varies"
    growth_outlook: str = "Growing"
    required_education: str = "Bachelor's"
    
    def to_vector(self) -> np.ndarray:
        """Convert feature dict to numpy vector."""
        return np.array([self.features.get(f, 0) for f in FEATURE_NAMES])


@dataclass
class Recommendation:
    """A single career recommendation."""
    rank: int
    career: str
    compatibility_score: float  # 0-100
    explanation: str
    feature_alignment: Dict[str, str]  # feature -> "high/good/low/critical"
    salary_range: str
    

FEATURE_NAMES = [
    'logical_thinking', 'creativity', 'communication',
    'problem_solving', 'teamwork', 'leadership',
    'math_quantitative', 'english_writing', 'science_technical',
    'art_visual_design', 'tech_affinity', 'business_acumen',
    'social_interaction', 'independence', 'work_life_commitment'
]

assert len(FEATURE_NAMES) == 15, "Must have exactly 15 features"

# ============================================================================
# CAREER DATABASE
# ============================================================================

CAREERS_DATA = {
    "Software Engineer": {
        "description": "Design, develop, and maintain software systems",
        "features": {
            'logical_thinking': 9.5, 'creativity': 7.0, 'communication': 7.0,
            'problem_solving': 9.0, 'teamwork': 8.0, 'leadership': 6.0,
            'math_quantitative': 8.0, 'english_writing': 7.0, 'science_technical': 7.5,
            'art_visual_design': 5.0, 'tech_affinity': 9.5, 'business_acumen': 5.0,
            'social_interaction': 6.0, 'independence': 8.0, 'work_life_commitment': 7.0,
        },
        'salary_range': '$80k - $150k',
        'growth_outlook': 'Excellent',
        'required_education': "Bachelor's in CS/Engineering",
    },
    "Data Scientist": {
        "description": "Analyze data to solve business problems",
        "features": {
            'logical_thinking': 9.5, 'creativity': 7.5, 'communication': 7.0,
            'problem_solving': 9.0, 'teamwork': 7.5, 'leadership': 6.0,
            'math_quantitative': 9.5, 'english_writing': 7.5, 'science_technical': 8.5,
            'art_visual_design': 4.0, 'tech_affinity': 8.5, 'business_acumen': 7.0,
            'social_interaction': 5.5, 'independence': 7.5, 'work_life_commitment': 6.0,
        },
        'salary_range': '$85k - $160k',
        'growth_outlook': 'Excellent',
        'required_education': "Bachelor's in Math/CS, Master's preferred",
    },
    "UX Designer": {
        "description": "Design user-friendly interfaces and experiences",
        "features": {
            'logical_thinking': 7.0, 'creativity': 9.0, 'communication': 8.5,
            'problem_solving': 8.0, 'teamwork': 8.5, 'leadership': 5.5,
            'math_quantitative': 5.0, 'english_writing': 7.0, 'science_technical': 5.0,
            'art_visual_design': 9.5, 'tech_affinity': 7.5, 'business_acumen': 6.0,
            'social_interaction': 8.0, 'independence': 7.0, 'work_life_commitment': 6.5,
        },
        'salary_range': '$70k - $130k',
        'growth_outlook': 'Very Good',
        'required_education': "Bachelor's in Design/HCI or bootcamp",
    },
    "Management Consultant": {
        "description": "Advise organizations on strategy and operations",
        "features": {
            'logical_thinking': 8.5, 'creativity': 7.5, 'communication': 9.5,
            'problem_solving': 9.0, 'teamwork': 8.5, 'leadership': 9.0,
            'math_quantitative': 7.5, 'english_writing': 8.5, 'science_technical': 4.5,
            'art_visual_design': 4.0, 'tech_affinity': 6.0, 'business_acumen': 9.5,
            'social_interaction': 9.0, 'independence': 7.5, 'work_life_commitment': 8.0,
        },
        'salary_range': '$90k - $200k+',
        'growth_outlook': 'Good',
        'required_education': "Bachelor's, MBA beneficial",
    },
    "Product Manager": {
        "description": "Lead product vision, strategy, and development",
        "features": {
            'logical_thinking': 8.5, 'creativity': 7.5, 'communication': 9.0,
            'problem_solving': 8.5, 'teamwork': 9.0, 'leadership': 9.0,
            'math_quantitative': 7.0, 'english_writing': 8.0, 'science_technical': 6.0,
            'art_visual_design': 6.5, 'tech_affinity': 7.5, 'business_acumen': 8.5,
            'social_interaction': 8.5, 'independence': 8.0, 'work_life_commitment': 7.5,
        },
        'salary_range': '$85k - $170k',
        'growth_outlook': 'Excellent',
        'required_education': "Bachelor's degree",
    },
    "Graphic Designer": {
        "description": "Create visual designs for various media",
        "features": {
            'logical_thinking': 6.0, 'creativity': 9.5, 'communication': 7.0,
            'problem_solving': 7.0, 'teamwork': 7.5, 'leadership': 4.5,
            'math_quantitative': 4.5, 'english_writing': 6.0, 'science_technical': 3.5,
            'art_visual_design': 9.5, 'tech_affinity': 7.0, 'business_acumen': 5.0,
            'social_interaction': 7.0, 'independence': 7.5, 'work_life_commitment': 6.0,
        },
        'salary_range': '$45k - $90k',
        'growth_outlook': 'Good',
        'required_education': "Bachelor's in Design or Portfolio-based",
    },
    "Teacher": {
        "description": "Educate and mentor students in academic subjects",
        "features": {
            'logical_thinking': 7.5, 'creativity': 7.0, 'communication': 9.0,
            'problem_solving': 7.5, 'teamwork': 7.5, 'leadership': 8.0,
            'math_quantitative': 7.0, 'english_writing': 8.5, 'science_technical': 7.0,
            'art_visual_design': 5.5, 'tech_affinity': 5.5, 'business_acumen': 4.5,
            'social_interaction': 9.5, 'independence': 6.5, 'work_life_commitment': 6.0,
        },
        'salary_range': '$40k - $70k',
        'growth_outlook': 'Stable',
        'required_education': "Bachelor's + Teaching Certification",
    },
    "Financial Analyst": {
        "description": "Analyze financial data and provide investment insights",
        "features": {
            'logical_thinking': 8.5, 'creativity': 5.5, 'communication': 7.0,
            'problem_solving': 8.5, 'teamwork': 7.0, 'leadership': 6.0,
            'math_quantitative': 9.5, 'english_writing': 7.5, 'science_technical': 5.0,
            'art_visual_design': 3.5, 'tech_affinity': 7.0, 'business_acumen': 9.0,
            'social_interaction': 6.5, 'independence': 7.0, 'work_life_commitment': 7.5,
        },
        'salary_range': '$70k - $150k',
        'growth_outlook': 'Good',
        'required_education': "Bachelor's in Finance/Accounting",
    },
    "DevOps Engineer": {
        "description": "Manage infrastructure and deployment pipelines",
        "features": {
            'logical_thinking': 8.5, 'creativity': 6.0, 'communication': 6.5,
            'problem_solving': 9.0, 'teamwork': 7.5, 'leadership': 5.5,
            'math_quantitative': 7.0, 'english_writing': 6.5, 'science_technical': 7.0,
            'art_visual_design': 3.5, 'tech_affinity': 9.0, 'business_acumen': 5.5,
            'social_interaction': 5.5, 'independence': 8.0, 'work_life_commitment': 7.0,
        },
        'salary_range': '$90k - $170k',
        'growth_outlook': 'Excellent',
        'required_education': "Bachelor's in CS, certifications valuable",
    },
    "Marketing Manager": {
        "description": "Develop and execute marketing strategies",
        "features": {
            'logical_thinking': 7.5, 'creativity': 8.0, 'communication': 9.0,
            'problem_solving': 8.0, 'teamwork': 8.5, 'leadership': 8.5,
            'math_quantitative': 7.0, 'english_writing': 8.5, 'science_technical': 4.0,
            'art_visual_design': 7.0, 'tech_affinity': 6.5, 'business_acumen': 8.5,
            'social_interaction': 9.0, 'independence': 7.5, 'work_life_commitment': 6.5,
        },
        'salary_range': '$70k - $130k',
        'growth_outlook': 'Good',
        'required_education': "Bachelor's degree",
    },
    # Add more careers...
    "Project Manager": {
        "description": "Plan and oversee project execution",
        "features": {
            'logical_thinking': 8.0, 'creativity': 6.0, 'communication': 8.5,
            'problem_solving': 8.0, 'teamwork': 9.0, 'leadership': 9.0,
            'math_quantitative': 7.0, 'english_writing': 7.5, 'science_technical': 5.0,
            'art_visual_design': 4.0, 'tech_affinity': 6.5, 'business_acumen': 7.5,
            'social_interaction': 8.5, 'independence': 7.0, 'work_life_commitment': 7.5,
        },
        'salary_range': '$75k - $140k',
        'growth_outlook': 'Good',
        'required_education': "Bachelor's degree, PMP/PRINCE2 beneficial",
    },
}

# ============================================================================
# QUIZ TO FEATURES MAPPING
# ============================================================================

QUIZ_TO_FEATURES = {
    # Logic questions (Q1-3)
    1: {'logical_thinking': 1.0, 'problem_solving': 0.3},
    2: {'logical_thinking': 0.8, 'problem_solving': 0.5},
    3: {'logical_thinking': 0.9, 'problem_solving': 0.6},
    
    # Creativity questions (Q4-6)
    4: {'creativity': 1.0, 'art_visual_design': 0.4},
    5: {'creativity': 0.9, 'art_visual_design': 0.5},
    6: {'creativity': 0.95, 'art_visual_design': 0.3},
    
    # Communication questions (Q7-9)
    7: {'communication': 1.0, 'social_interaction': 0.4},
    8: {'communication': 0.9, 'social_interaction': 0.5},
    9: {'communication': 0.95, 'english_writing': 0.3},
    
    # Academic questions (Q10-13)
    10: {'math_quantitative': 1.0, 'logical_thinking': 0.2},
    11: {'english_writing': 1.0, 'communication': 0.2},
    12: {'science_technical': 1.0, 'problem_solving': 0.2},
    13: {'art_visual_design': 0.8, 'creativity': 0.3},
    
    # Interest questions (Q14-17)
    14: {'tech_affinity': 1.0, 'logical_thinking': 0.3},
    15: {'business_acumen': 1.0, 'leadership': 0.3},
    16: {'creativity': 0.8, 'art_visual_design': 0.7},
    17: {'social_interaction': 1.0, 'teamwork': 0.5},
    
    # Work style questions (Q18-19)
    18: {'independence': 1.0, 'leadership': 0.5},
    19: {'teamwork': 1.0, 'social_interaction': 0.3},
}

# ============================================================================
# USER FEATURE EXTRACTOR
# ============================================================================

class UserFeatureExtractor:
    """Convert quiz answers to feature vectors."""
    
    @staticmethod
    def extract_features(quiz_answers: Dict[int, int]) -> Dict[str, float]:
        """
        Convert quiz answers (Q1-19, each answer 1-10) to feature vector.
        
        Args:
            quiz_answers: {question_id: answer_value}
                         where question_id in [1-19], answer_value in [1-10]
        
        Returns:
            {feature_name: score} where score in [0-10]
        """
        # Initialize feature accumulator
        feature_sums = {f: 0 for f in FEATURE_NAMES}
        feature_counts = {f: 0 for f in FEATURE_NAMES}
        
        # Aggregate quiz answers into features
        for question_id, answer_value in quiz_answers.items():
            if question_id not in QUIZ_TO_FEATURES:
                continue
            
            # Each quiz answer contributes to multiple features
            feature_contributions = QUIZ_TO_FEATURES[question_id]
            for feature_name, weight in feature_contributions.items():
                contribution = answer_value * weight
                feature_sums[feature_name] += contribution
                feature_counts[feature_name] += weight
        
        # Compute average and normalize
        user_features = {}
        for feature_name in FEATURE_NAMES:
            if feature_counts[feature_name] > 0:
                avg = feature_sums[feature_name] / feature_counts[feature_name]
                user_features[feature_name] = min(10.0, max(0.0, avg))
            else:
                user_features[feature_name] = 5.0  # Default neutral
        
        logger.info(f"Extracted user features: {user_features}")
        return user_features
    
    @staticmethod
    def features_to_vector(features: Dict[str, float]) -> np.ndarray:
        """Convert feature dict to normalized numpy vector."""
        vector = np.array([features.get(f, 0) for f in FEATURE_NAMES])
        # Normalize (L2 norm)
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector


# ============================================================================
# RECOMMENDATION ENGINE
# ============================================================================

class RecommendationEngine:
    """Similarity-based career recommendation engine."""
    
    def __init__(self):
        """Initialize with career database."""
        self.careers: Dict[str, Career] = {}
        self._load_careers()
    
    def _load_careers(self):
        """Load careers from data dictionary."""
        for name, data in CAREERS_DATA.items():
            career = Career(
                id=name.lower().replace(' ', '_'),
                name=name,
                description=data['description'],
                features=data['features'],
                salary_range=data['salary_range'],
                growth_outlook=data['growth_outlook'],
                required_education=data['required_education'],
            )
            self.careers[name] = career
    
    def recommend(self, user_features: Dict[str, float], top_n: int = 5) -> List[Recommendation]:
        """
        Generate top-N career recommendations for user.
        
        Args:
            user_features: Dict of feature scores from quiz
            top_n: Number of recommendations to return (default 5)
        
        Returns:
            List of Recommendation objects sorted by compatibility
        """
        # Convert user features to normalized vector
        user_vector = UserFeatureExtractor.features_to_vector(user_features)
        
        # Compute similarity with each career
        similarities = []
        for career_name, career in self.careers.items():
            career_vector = career.to_vector()
            # Normalize career vector
            norm = np.linalg.norm(career_vector)
            if norm > 0:
                career_vector = career_vector / norm
            
            # Cosine similarity
            similarity = np.dot(user_vector, career_vector)
            compatibility = max(0, similarity * 100)  # Scale to 0-100
            
            similarities.append((career_name, compatibility, user_vector, career_vector))
        
        # Sort by compatibility descending
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Generate recommendations with explanations
        recommendations = []
        for rank, (career_name, compatibility, user_vec, career_vec) in enumerate(similarities[:top_n], 1):
            career = self.careers[career_name]
            explanation = self._generate_explanation(
                career_name, compatibility, user_features, career.features
            )
            feature_alignment = self._compute_alignment(user_features, career.features)
            
            rec = Recommendation(
                rank=rank,
                career=career_name,
                compatibility_score=round(compatibility, 1),
                explanation=explanation,
                feature_alignment=feature_alignment,
                salary_range=career.salary_range,
            )
            recommendations.append(rec)
        
        logger.info(f"Generated {len(recommendations)} recommendations")
        return recommendations
    
    def _compute_alignment(self, user_features: Dict[str, float], 
                          career_features: Dict[str, float]) -> Dict[str, str]:
        """Classify each feature as high/good/low/critical match."""
        alignment = {}
        for feature_name in FEATURE_NAMES:
            user_score = user_features.get(feature_name, 5)
            career_score = career_features.get(feature_name, 5)
            
            # Compute difference
            diff = user_score - career_score
            
            # Classify
            if diff >= 1.5:  # User significantly above career requirement
                alignment[feature_name] = "high_exceed"
            elif diff >= 0.5:  # User above requirement
                alignment[feature_name] = "good_exceed"
            elif diff >= -0.5:  # Well matched
                alignment[feature_name] = "good_match"
            elif diff >= -1.5:  # Below requirement
                alignment[feature_name] = "low_match"
            else:  # Significantly below
                alignment[feature_name] = "critical_gap"
        
        return alignment
    
    def _generate_explanation(self, career_name: str, compatibility: float,
                             user_features: Dict[str, float],
                             career_features: Dict[str, float]) -> str:
        """Generate human-readable explanation of the recommendation."""
        
        # Find top matching and mismatching features
        feature_scores = {}
        for feature_name in FEATURE_NAMES:
            user_score = user_features.get(feature_name, 5)
            career_score = career_features.get(feature_name, 5)
            # Absolute alignment (higher better)
            alignment = 10 - abs(user_score - career_score)
            feature_scores[feature_name] = {
                'user': user_score,
                'career': career_score,
                'alignment': alignment
            }
        
        # Identify top strengths (high alignment)
        top_matches = sorted(
            feature_scores.items(), 
            key=lambda x: x[1]['alignment'], 
            reverse=True
        )[:3]
        
        # Identify areas to develop (low alignment)
        gaps = sorted(
            feature_scores.items(), 
            key=lambda x: x[1]['alignment']
        )[:2]
        
        # Build explanation
        explanation_parts = [
            f"{career_name} is a strong match ({compatibility:.0f}% compatibility) for you."
        ]
        
        # Highlight strengths
        strengths = []
        for feature_name, scores in top_matches:
            if scores['alignment'] > 7:
                strengths.append(f"{feature_name.replace('_', ' ').title()}")
        if strengths:
            explanation_parts.append(
                f"Your strengths in {', '.join(strengths)} align great with this role."
            )
        
        # Mention development areas
        dev_areas = []
        for feature_name, scores in gaps:
            if scores['alignment'] < 6 and scores['user'] < scores['career']:
                dev_areas.append(f"{feature_name.replace('_', ' ').title()}")
        if dev_areas:
            explanation_parts.append(
                f"Consider developing: {', '.join(dev_areas)}."
            )
        
        return " ".join(explanation_parts)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example: Simulate a tech-oriented student
    example_quiz = {
        1: 9, 2: 8, 3: 9,      # Logic: high
        4: 5, 5: 4, 6: 4,      # Creativity: low
        7: 6, 8: 7, 9: 6,      # Communication: moderate
        10: 8, 11: 6, 12: 8, 13: 4,  # Academic: decent
        14: 10, 15: 5, 16: 3, 17: 4,  # Interests: tech-focused
        18: 8, 19: 6,          # Work style: independent + some teamwork
    }
    
    print("=" * 70)
    print("CAREER RECOMMENDATION ENGINE - DEMO")
    print("=" * 70)
    
    # Extract user features
    extractor = UserFeatureExtractor()
    user_features = extractor.extract_features(example_quiz)
    
    print("\n📋 USER PROFILE:")
    print("-" * 70)
    for feature, score in sorted(user_features.items()):
        print(f"  {feature.replace('_', ' ').title():25} {score:5.1f}/10")
    
    # Generate recommendations
    engine = RecommendationEngine()
    recommendations = engine.recommend(user_features, top_n=5)
    
    print("\n\n🎯 TOP 5 CAREER RECOMMENDATIONS:")
    print("-" * 70)
    for rec in recommendations:
        print(f"\n#{rec.rank} - {rec.career}")
        print(f"     Compatibility: {rec.compatibility_score}%")
        print(f"     Salary: {rec.salary_range}")
        print(f"     {rec.explanation}")
    
    print("\n" + "=" * 70)
