"""
Ability-Based Recommendation Engine
Matches user abilities/interests against career ability requirements

This is the primary recommendation system that should be used instead of
the old classification-based approach.
"""
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from django.db.models import QuerySet
from apps.careers.models import Career


# Mapping from quiz dimensions to ability vector dimensions
# Quiz answers are on 0-10 scale, ability vector is 0-10 scale
QUIZ_TO_ABILITY_MAPPING = {
    # Cognitive abilities
    "logical_thinking": 0,      # Dimension 0: Logical thinking
    "analytical_skills": 0,      # Also maps to logical thinking
    "mathematical_ability": 1,   # Dimension 1: Mathematical
    "problem_solving": 0,        # Also logical thinking
    
    # Creative abilities
    "creativity": 2,             # Dimension 2: Creativity
    "artistic_ability": 2,       # Also creativity
    "design_thinking": 2,        # Also creativity
    
    # Communication
    "communication": 3,          # Dimension 3: Communication
    "writing": 3,                # Also communication
    "presentation_skills": 3,    # Also communication
    
    # Leadership
    "leadership": 4,             # Dimension 4: Leadership
    "teamwork": 4,               # Also leadership
    "collaboration": 4,          # Also leadership
    
    # Management
    "management": 5,             # Dimension 5: Management/Organization
    "organization": 5,           # Also management
    "time_management": 5,        # Also management
    
    # Technical
    "technical_skills": 6,       # Dimension 6: Technical aptitude
    "programming": 6,            # Also technical
    "engineering_thinking": 6,   # Also technical
    
    # Detail orientation
    "attention_to_detail": 7,    # Dimension 7: Attention to detail
    "precision": 7,              # Also detail
    
    # Research/Analysis
    "research_ability": 8,       # Dimension 8: Research ability
    "data_analysis": 8,          # Also research
    
    # Interpersonal
    "interpersonal_skills": 9,   # Dimension 9: Interpersonal skills
    "empathy": 9,                # Also interpersonal
    "customer_service": 9,       # Also interpersonal
    
    # Resilience
    "stress_tolerance": 10,      # Dimension 10: Stress tolerance/Resilience
    "adaptability": 10,          # Also resilience
    
    # Learning agility
    "learning_ability": 11,      # Dimension 11: Learning/Growth mindset
    "continuous_learning": 11,   # Also learning
    
    # Domain knowledge
    "domain_knowledge": 12,      # Dimension 12: Subject matter expertise
    "industry_knowledge": 12,    # Also domain knowledge
    
    # Physical/Hands-on
    "hands_on_skills": 13,       # Dimension 13: Hands-on/Practical skills
    "physical_ability": 13,      # Also hands-on
    
    # Business acumen
    "business_acumen": 14,       # Dimension 14: Business understanding
    "financial_literacy": 14,    # Also business
}


@dataclass
class AbilityRecommendation:
    """Recommendation based on ability matching."""
    career: Career
    match_score: float          # 0-1, overall match quality
    ability_match_score: float  # 0-1, how well user abilities match career needs
    coverage_score: float       # 0-1, how many career abilities user can cover
    is_strength_match: bool     # True if match is in user's strong areas
    top_matching_abilities: List[str]  # Top 3 abilities that match
    missing_abilities: List[str]       # Abilities user is weak in but career needs
    salary_range: str
    job_growth: str
    explanation: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API response."""
        return {
            "name": self.career.name,
            "description": self.career.description,
            "compatibility_score": round(self.match_score * 100, 2),
            "ability_match_score": round(self.ability_match_score * 100, 2),
            "coverage_score": round(self.coverage_score * 100, 2),
            "is_strength_match": self.is_strength_match,
            "top_matching_abilities": self.top_matching_abilities,
            "missing_abilities": self.missing_abilities,
            "required_skills": self.career.required_skills,
            "salary_range": self.salary_range,
            "job_growth": self.job_growth,
            "explanation": self.explanation,
            "cluster": self.career.cluster,
        }


ABILITY_NAMES = [
    "Logical Thinking",
    "Mathematical",
    "Creativity",
    "Communication",
    "Leadership",
    "Management",
    "Technical",
    "Attention to Detail",
    "Research",
    "Interpersonal",
    "Resilience",
    "Learning",
    "Domain Knowledge",
    "Hands-on",
    "Business Acumen",
]


class AbilityRecommendationService:
    """
    Recommendation engine based on ability matching.
    Matches user abilities against career ability requirements.
    """

    def __init__(self):
        """Initialize the service."""
        self.ability_names = ABILITY_NAMES
        self.quiz_to_ability = QUIZ_TO_ABILITY_MAPPING

    def extract_user_abilities(self, quiz_answers: Dict) -> np.ndarray:
        """
        Convert quiz answers to 15-dimensional ability vector.
        
        Maps quiz answers to ability dimensions based on question metadata.
        If category is provided in the answers dict, use it; otherwise infer from question ID.
        
        Args:
            quiz_answers: Dict of quiz question answers (0-10 scale)
            Can be: {"question_id": value} or {"question_id": {"value": score, "category": "logic"}}
            
        Returns:
            15-dimensional numpy array (0-10 scale) representing user abilities
        """
        # Map quiz categories to ability dimensions
        category_to_ability = {
            'logic': [0],  # Logical Thinking
            'creativity': [2],  # Creativity
            'communication': [3, 9],  # Communication, Interpersonal
            'academic': [0, 1],  # Logical + Mathematical
            'interests': [2, 6, 12],  # Creativity, Technical, Domain
            'work_style': [4, 5, 10],  # Leadership, Management, Resilience
        }
        
        # Initialize ability vector
        abilities = np.zeros(15)
        ability_counts = np.zeros(15)
        
        # Try to fetch full question objects for category information
        try:
            from apps.quiz.models import QuizQuestion
            
            # Build a map of question ID to category
            question_categories = {}
            for q in QuizQuestion.objects.all():
                question_categories[str(q.id)] = q.category
        except Exception:
            # If we can't fetch questions, use fallback method
            question_categories = {}
        
        # Process each answer
        for question_id, answer_value in quiz_answers.items():
            question_id_str = str(question_id)
            
            try:
                # Get score value (might be nested)
                if isinstance(answer_value, dict):
                    score = float(answer_value.get('value', answer_value.get('score', 5)))
                    category = answer_value.get('category', question_categories.get(question_id_str, 'interests'))
                else:
                    score = float(answer_value)
                    category = question_categories.get(question_id_str, 'interests')
                
                # Map category to ability dimensions
                ability_dims = category_to_ability.get(category, [2, 6])  # Default to Creativity, Technical
                
                # Assign score to mapped dimensions
                for dim_idx in ability_dims:
                    if 0 <= dim_idx < 15:
                        abilities[dim_idx] += score
                        ability_counts[dim_idx] += 1
                        
            except (ValueError, TypeError):
                # Skip invalid answers
                continue
        
        # Average repeated dimensions
        for i in range(len(abilities)):
            if ability_counts[i] > 0:
                abilities[i] = abilities[i] / ability_counts[i]
        
        # If no valid answers, return neutral profile (5.0 across all dimensions)
        if np.sum(abilities) == 0:
            abilities = np.ones(15) * 5.0
        
        return np.clip(abilities, 0, 10)

    def calculate_ability_match(
        self,
        user_abilities: np.ndarray,
        career_abilities: np.ndarray,
    ) -> Tuple[float, float, List[str], List[str]]:
        """
        Calculate how well user abilities match career requirements.
        
        Returns:
            (match_score, coverage_score, top_abilities, missing_abilities)
        """
        match_scores = []
        
        # Calculate match for each ability dimension
        for i in range(len(career_abilities)):
            career_need = career_abilities[i]
            user_ability = user_abilities[i]
            
            if career_need > 0:
                # How well does user meet this requirement?
                # Perfect match at user_ability >= career_need
                match = max(0, min(1.0, user_ability / max(1, career_need)))
                match_scores.append(match)
        
        # Overall match: average of all dimensions
        match_score = float(np.mean(match_scores)) if match_scores else 0.5
        
        # Coverage: what percentage of career needs can user meet?
        career_needed_count = np.sum(career_abilities > 0)
        user_meets_count = np.sum(
            (career_abilities > 0) & (user_abilities >= career_abilities * 0.8)
        )
        coverage = user_meets_count / max(1, career_needed_count)
        
        # Find top matching abilities
        top_abilities = []
        for i in range(len(career_abilities)):
            if career_abilities[i] > 5:  # Career requires this ability
                if user_abilities[i] >= career_abilities[i]:
                    top_abilities.append(self.ability_names[i])
        top_abilities = top_abilities[:3]
        
        # Find missing abilities
        missing = []
        for i in range(len(career_abilities)):
            if career_abilities[i] > 7:  # Career heavily requires this
                if user_abilities[i] < career_abilities[i] * 0.7:
                    missing.append(self.ability_names[i])
        missing = missing[:3]
        
        return match_score, coverage, top_abilities, missing

    def get_career_explanations(self, career: Career) -> str:
        """Generate explanation connecting user abilities to career."""
        abilities = career.ability_vector
        
        primary_abilities = []
        for i, val in enumerate(abilities[:10]):  # First 10 primary abilities
            if val > 7:
                primary_abilities.append(self.ability_names[i])
        
        if primary_abilities:
            explanation = f"This career requires strong skills in {', '.join(primary_abilities[:2])}. "
        else:
            explanation = f"{career.name} is a {career.cluster.lower()} role. "
        
        explanation += f"{career.description if career.description else 'Dynamic role with growth potential.'}"
        
        return explanation

    def recommend(
        self,
        quiz_answers: Dict,
        top_n: int = 5,
        diversity: bool = True,
    ) -> List[AbilityRecommendation]:
        """
        Generate career recommendations based on user abilities.
        
        Args:
            quiz_answers: Dict of quiz answers (question -> 0-10 score)
            top_n: Number of recommendations to return
            diversity: If True, limit 1 career per cluster in top N
            
        Returns:
            List of AbilityRecommendation objects sorted by match score
        """
        # Extract user abilities from quiz answers
        user_abilities = self.extract_user_abilities(quiz_answers)
        
        # Get all careers with ability vectors
        careers = Career.objects.filter(ability_vector__isnull=False).exclude(
            ability_vector=[]
        )
        
        recommendations = []
        
        for career in careers:
            try:
                career_abilities = np.array(career.ability_vector)
                
                # Calculate match
                match_score, coverage, top_abs, missing = self.calculate_ability_match(
                    user_abilities, career_abilities
                )
                
                # Boost score if this is a strength match
                is_strength = match_score > 0.75
                if is_strength:
                    match_score = min(1.0, match_score * 1.1)
                
                # Create recommendation
                rec = AbilityRecommendation(
                    career=career,
                    match_score=match_score,
                    ability_match_score=match_score,
                    coverage_score=coverage,
                    is_strength_match=is_strength,
                    top_matching_abilities=top_abs,
                    missing_abilities=missing,
                    salary_range=career.average_salary_range or "Unknown",
                    job_growth=career.job_growth or "N/A",
                    explanation=self.get_career_explanations(career),
                )
                
                recommendations.append(rec)
                
            except (ValueError, TypeError):
                # Skip careers with invalid ability vectors
                continue
        
        # Sort by match score
        recommendations.sort(key=lambda x: x.match_score, reverse=True)
        
        # Apply diversity constraint if requested
        if diversity:
            diverse_recs = []
            clusters_used = set()
            
            for rec in recommendations:
                if rec.career.cluster not in clusters_used:
                    diverse_recs.append(rec)
                    clusters_used.add(rec.career.cluster)
                    if len(diverse_recs) >= top_n:
                        break
            
            recommendations = diverse_recs
        else:
            recommendations = recommendations[:top_n]
        
        return recommendations
