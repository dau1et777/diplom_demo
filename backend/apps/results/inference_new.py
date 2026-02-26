"""
ML Inference Service - NEW Similarity-Based Recommendation Engine

Bridges Django with the new feature-vector recommendation system.
This replaces the old RandomForest classifier approach.
"""

import logging
from typing import Dict, List
from django.conf import settings
from ml.recommendation_engine import (
    UserFeatureExtractor,
    RecommendationEngine,
    FEATURE_NAMES
)

logger = logging.getLogger(__name__)


class CareerInferenceService:
    """
    Service for generating career recommendations using similarity matching.
    Handles feature extraction from quiz answers and ranking.
    """
    
    FEATURE_NAMES = FEATURE_NAMES
    
    def __init__(self):
        """Initialize the recommendation engine."""
        try:
            self.engine = RecommendationEngine()
            self.extractor = UserFeatureExtractor()
            logger.info("CareerInferenceService (Similarity-Based) initialized")
        except Exception as e:
            logger.error(f"Failed to initialize recommendation engine: {e}")
            raise
    
    def extract_features_from_quiz(self, quiz_answers: dict) -> dict:
        """
        Extract feature vector from quiz question responses.
        
        Maps the 19 quiz questions to 15 feature dimensions using domain knowledge.
        
        Args:
            quiz_answers: Dict of {question_id: response_value} where:
                         - question_id: string UUID of quiz question
                         - response_value: 1-10 (user's answer)
        
        Returns:
            Dict with 15 extracted features, each 0-10 scale
            Example: {
                'logical_thinking': 8.5,
                'creativity': 6.2,
                ...
            }
        """
        from apps.quiz.models import QuizQuestion
        
        # Convert question IDs to numeric indices (Q1-19)
        numeric_answers = {}
        questions = QuizQuestion.objects.all().order_by('order')
        
        for idx, question in enumerate(questions, 1):
            question_id_str = str(question.id)
            if question_id_str in quiz_answers:
                numeric_answers[idx] = int(quiz_answers[question_id_str])
        
        if len(numeric_answers) < 15:  # Require at least 15/19 answers
            logger.warning(f"Incomplete quiz: only {len(numeric_answers)}/19 answered")
        
        # Extract features using the new extractor
        features = self.extractor.extract_features(numeric_answers)
        
        logger.info(f"Extracted features from {len(numeric_answers)} quiz answers")
        logger.debug(f"Features: {features}")
        
        return features
    
    def predict_careers(self, quiz_answers: dict, top_n: int = 5) -> List[dict]:
        """
        Generate top-N career recommendations based on quiz answers.
        
        Args:
            quiz_answers: Dict of {question_id: response_value}
            top_n: Number of recommendations (default 5)
        
        Returns:
            List of dicts with format:
            [
                {
                    'career': 'Career Name',
                    'compatibility_score': 87.5,
                    'explanation': 'Human-readable explanation...',
                    'feature_alignment': {...details...},
                    'salary_range': '$70k - $130k'
                },
                ...
            ]
        """
        try:
            # Extract user features from quiz
            user_features = self.extract_features_from_quiz(quiz_answers)
            
            # Get recommendations using similarity matching
            recommendations = self.engine.recommend(user_features, top_n=top_n)
            
            # Convert to dict format for Django serialization
            result = []
            for rec in recommendations:
                result.append({
                    'career': rec.career,
                    'compatibility_score': rec.compatibility_score,
                    'explanation': rec.explanation,
                    'feature_alignment': rec.feature_alignment,
                    'salary_range': rec.salary_range,
                    'rank': rec.rank,
                })
            
            logger.info(f"Generated {len(result)} recommendations")
            return result
        
        except Exception as e:
            logger.error(f"Error in predict_careers: {e}", exc_info=True)
            raise
    
    def calculate_ability_scores(self, quiz_answers: dict) -> dict:
        """
        Calculate aggregated ability scores for user dashboard.
        
        Args:
            quiz_answers: Dict of quiz responses
        
        Returns:
            Dict of aggregated scores (each 0-10):
            {
                'logical_thinking': 8.5,
                'creativity': 6.0,
                ...
                'overall': 7.2  (average)
            }
        """
        try:
            user_features = self.extract_features_from_quiz(quiz_answers)
            
            # Compute overall average
            overall_score = sum(user_features.values()) / len(user_features)
            
            abilities = dict(user_features)
            abilities['overall'] = round(overall_score, 1)
            
            logger.debug(f"Calculated ability scores: {abilities}")
            return abilities
        
        except Exception as e:
            logger.error(f"Error in calculate_ability_scores: {e}")
            raise


# Singleton instance
_inference_service = None

def get_inference_service() -> CareerInferenceService:
    """Get or create singleton inference service."""
    global _inference_service
    if _inference_service is None:
        _inference_service = CareerInferenceService()
    return _inference_service
