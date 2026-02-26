"""
ML Inference Service for Career Recommendations
Bridges Django with sklearn model for predictions.
"""

import logging
import numpy as np
from django.conf import settings
from ml.predictor import CareerPredictor, get_career_explanation


logger = logging.getLogger(__name__)


class CareerInferenceService:
    """
    Service for generating career recommendations using trained ML model.
    Handles feature extraction from quiz answers and prediction.
    """
    
    # Feature order must match training dataset
    FEATURE_SEQUENCE = [
        'logical_thinking', 'creativity', 'communication', 'problem_solving',
        'teamwork', 'leadership', 'math_score', 'english_score', 'science_score',
        'art_score', 'interest_tech', 'interest_business', 'interest_creativity',
        'interest_social', 'work_style_independent', 'work_style_collaborative'
    ]
    
    def __init__(self):
        """Initialize the ML predictor."""
        try:
            self.predictor = CareerPredictor(model_dir=settings.ML_MODELS_DIR)
            logger.info("CareerPredictor initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize CareerPredictor: {e}")
            raise
    
    def extract_features_from_quiz(self, quiz_answers: dict) -> dict:
        """
        Extract feature vector from quiz question responses.
        Maps quiz responses to model features based on question categories.
        
        Args:
            quiz_answers: Dict of question_id: response_value (1-10 scale)
            
        Returns:
            Dict with extracted features (0-10 scale, then normalized by scaler)
        """
        from apps.quiz.models import QuizQuestion
        
        logger.info(f"DEBUG: Raw quiz answers: {quiz_answers}")
        
        # Initialize feature dict with empty lists to collect values for averaging
        features_raw = {
            'logical_thinking': [],
            'creativity': [],
            'communication': [],
            'problem_solving': [],
            'teamwork': [],
            'leadership': [],
            'math_score': [],
            'english_score': [],
            'science_score': [],
            'art_score': [],
            'interest_tech': [],
            'interest_business': [],
            'interest_creativity': [],
            'interest_social': [],
            'work_style_independent': [],
            'work_style_collaborative': [],
        }
        
        # Map question categories to features
        category_feature_map = {
            'logic': 'logical_thinking',
            'creativity': 'creativity',
            'communication': 'communication',
            'academic': None,  # Special handling - breaks into sub-features
            'interests': None,  # Special handling - breaks into sub-features
            'work_style': None,  # Special handling - breaks into sub-features
        }
        
        # Fetch all quiz questions to get their categories and order
        try:
            all_questions = {str(q.id): q for q in QuizQuestion.objects.all()}
        except Exception as e:
            logger.error(f"Error fetching questions: {e}")
            all_questions = {}
        
        # Process each answer
        for question_id_str, response_value in quiz_answers.items():
            if question_id_str not in all_questions:
                continue
            
            question = all_questions[question_id_str]
            category = question.category
            order = question.order
            
            # Map by category
            if category == 'logic':
                features_raw['logical_thinking'].append(response_value)
            elif category == 'creativity':
                features_raw['creativity'].append(response_value)
            elif category == 'communication':
                features_raw['communication'].append(response_value)
                # Communication order 2 (leading) contributes to leadership
                if order == 8:  # "Are you comfortable working with and leading people?"
                    features_raw['leadership'].append(response_value)
                    features_raw['teamwork'].append(response_value)
            elif category == 'academic':
                # Q10: math, Q11: science, Q12: english, Q13: art
                if order == 10:
                    features_raw['math_score'].append(response_value)
                elif order == 11:
                    features_raw['science_score'].append(response_value)
                elif order == 12:
                    features_raw['english_score'].append(response_value)
                elif order == 13:
                    features_raw['art_score'].append(response_value)
            elif category == 'interests':
                # Q14: tech, Q15: business, Q16: creativity, Q17: social
                if order == 14:
                    features_raw['interest_tech'].append(response_value)
                elif order == 15:
                    features_raw['interest_business'].append(response_value)
                elif order == 16:
                    features_raw['interest_creativity'].append(response_value)
                elif order == 17:
                    features_raw['interest_social'].append(response_value)
            elif category == 'work_style':
                # Q18: independent, Q19: collaborative
                if order == 18:
                    features_raw['work_style_independent'].append(response_value)
                elif order == 19:
                    features_raw['work_style_collaborative'].append(response_value)
        
        # Calculate averages and fill in missing values
        features = {}
        for feature_name, values in features_raw.items():
            if values:
                avg = sum(values) / len(values)
                features[feature_name] = round(avg, 2)
            else:
                # Default to middle value if no answers for this feature
                features[feature_name] = 5.0
        
        # Infer problem_solving from logic and communication
        if features_raw['logical_thinking'] and features_raw['communication']:
            features['problem_solving'] = round(
                (sum(features_raw['logical_thinking']) / len(features_raw['logical_thinking'])
                 + sum(features_raw['communication']) / len(features_raw['communication'])) / 2,
                2
            )
        elif features_raw['logical_thinking']:
            features['problem_solving'] = round(
                sum(features_raw['logical_thinking']) / len(features_raw['logical_thinking']),
                2
            )
        
        # Infer teamwork from communication and collaborative work style
        if features_raw['communication'] and features_raw['work_style_collaborative']:
            features['teamwork'] = round(
                (sum(features_raw['communication']) / len(features_raw['communication'])
                 + sum(features_raw['work_style_collaborative']) / len(features_raw['work_style_collaborative'])) / 2,
                2
            )
        elif features_raw['work_style_collaborative']:
            features['teamwork'] = round(
                sum(features_raw['work_style_collaborative']) / len(features_raw['work_style_collaborative']),
                2
            )
        
        # If leadership not set from communication, infer from teamwork
        if not features_raw['leadership']:
            features['leadership'] = features.get('teamwork', 5.0)
        
        logger.info(f"DEBUG: Extracted features: {features}")
        return features
    
    def get_numeric_features_array(self, features: dict) -> np.ndarray:
        """
        Convert feature dict to normalized numpy array in correct order.
        
        Args:
            features: Dict with feature names and values
            
        Returns:
            Numpy array with features in order
        """
        feature_array = np.array([
            features.get(feat_name, 0) 
            for feat_name in self.FEATURE_SEQUENCE
        ], dtype=np.float32)
        
        logger.info(f"DEBUG: Feature array (before scaling): {feature_array}")
        logger.info(f"DEBUG: Feature sequence: {self.FEATURE_SEQUENCE}")
        
        return feature_array
    
    def predict_careers(self, quiz_answers: dict, top_n: int = 5) -> list:
        """
        Generate career recommendations for quiz answers.
        
        Args:
            quiz_answers: Dict of question_id: response_value
            top_n: Number of recommendations to return
            
        Returns:
            List of dicts with career and compatibility data
        """
        try:
            # Extract features from quiz and convert to array in correct order
            features = self.extract_features_from_quiz(quiz_answers)
            logger.debug(f"Extracted features dict: {features}")
            feature_array = self.get_numeric_features_array(features)
            logger.debug(f"Feature array (inference FEATURE_SEQUENCE order): {feature_array}")

            # Align to model feature names/order if predictor has feature_names
            model_feature_names = self.predictor.get_feature_names()
            if model_feature_names:
                # If model expects different ordering, build aligned array
                if model_feature_names != self.FEATURE_SEQUENCE:
                    logger.warning("Feature name/order mismatch between inference and model. Aligning to model order.")
                aligned_array = np.array([features.get(name, 5.0) for name in model_feature_names], dtype=np.float32)
                logger.debug(f"Final feature array aligned to model order: {aligned_array}")
            else:
                aligned_array = feature_array

            # Use predictor which will align feature names and scale properly
            recommendations = self.predictor.predict_top_careers(aligned_array, top_n=top_n)
            
            # Add explanations
            for rec in recommendations:
                explanation = get_career_explanation(rec['career'])
                rec['explanation'] = explanation['description']
                rec['required_skills'] = explanation['required_skills']
                rec['suitable_for'] = explanation['suitable_for']
            
            logger.info(f"Generated {len(recommendations)} career recommendations")
            return recommendations
        
        except Exception as e:
            logger.error(f"Error during career prediction: {e}")
            raise
    
    def calculate_ability_scores(self, quiz_answers: dict) -> dict:
        """
        Calculate user ability scores from quiz answers.
        
        Args:
            quiz_answers: Dict of question_id: response_value
            
        Returns:
            Dict with ability scores (avg of relevant questions)
        """
        from apps.quiz.models import QuizQuestion
        
        ability_scores = {
            'logical_thinking': 0,
            'creativity': 0,
            'communication': 0,
            'problem_solving': 0,
            'teamwork': 0,
            'leadership': 0,
            'academic_performance': 0,
            # interest breakdown will be added below
            'interest_tech': 0,
            'interest_business': 0,
            'interest_creativity': 0,
            'interest_social': 0,
        }
        
        # Fetch all questions
        try:
            all_questions = {str(q.id): q for q in QuizQuestion.objects.all()}
        except Exception as e:
            logger.error(f"Error fetching questions: {e}")
            return ability_scores
        
        # Group answers by category
        category_answers = {
            'logic': [],
            'creativity': [],
            'communication': [],
            'academic': [],
            'interests': [],
            'work_style': [],
        }
        # we'll also track interest details by question order
        interest_details = {
            14: [],  # tech
            15: [],  # business
            16: [],  # creativity
            17: [],  # social
        }
        
        for question_id_str, response_value in quiz_answers.items():
            if question_id_str not in all_questions:
                continue
            
            question = all_questions[question_id_str]
            category = question.category
            order = question.order
            
            if category in category_answers:
                category_answers[category].append(response_value)
            if category == 'interests' and order in interest_details:
                interest_details[order].append(response_value)
        
        # Calculate averages for each ability
        if category_answers['logic']:
            ability_scores['logical_thinking'] = round(
                sum(category_answers['logic']) / len(category_answers['logic']), 1
            )
        
        if category_answers['creativity']:
            ability_scores['creativity'] = round(
                sum(category_answers['creativity']) / len(category_answers['creativity']), 1
            )
        
        if category_answers['communication']:
            ability_scores['communication'] = round(
                sum(category_answers['communication']) / len(category_answers['communication']), 1
            )
        
        # Problem-solving: mix of logic and academic
        logic_avg = (sum(category_answers['logic']) / len(category_answers['logic'])) if category_answers['logic'] else 5
        academic_avg = (sum(category_answers['academic']) / len(category_answers['academic'])) if category_answers['academic'] else 5
        ability_scores['problem_solving'] = round((logic_avg + academic_avg) / 2, 1)
        
        # Teamwork: communication and work style
        comm_avg = (sum(category_answers['communication']) / len(category_answers['communication'])) if category_answers['communication'] else 5
        ability_scores['teamwork'] = round(comm_avg, 1)
        
        # Leadership: communication and interests
        ability_scores['leadership'] = round(comm_avg, 1)
        
        # Academic: average of academic category
        if category_answers['academic']:
            ability_scores['academic_performance'] = round(
                sum(category_answers['academic']) / len(category_answers['academic']), 1
            )
        
        # Interest-specific scores
        def avg_or_default(lst):
            return round(sum(lst) / len(lst), 1) if lst else 5.0
        ability_scores['interest_tech'] = avg_or_default(interest_details[14])
        ability_scores['interest_business'] = avg_or_default(interest_details[15])
        ability_scores['interest_creativity'] = avg_or_default(interest_details[16])
        ability_scores['interest_social'] = avg_or_default(interest_details[17])
        
        logger.info(f"DEBUG: Ability scores (with interests): {ability_scores}")
        return ability_scores
