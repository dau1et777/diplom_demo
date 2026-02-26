"""
Career Recommendation Inference Engine
Loads trained model and provides predictions with confidence scores.
"""

import os
import joblib
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class CareerPredictor:
    """
    Loads and uses trained model for career predictions.
    Provides compatibility percentages and explanations.
    """

    def __init__(self, model_dir='ml/models'):
        """
        Initialize predictor with saved model artifacts.
        
        Args:
            model_dir: Directory containing trained model files
        """
        self.model_dir = model_dir
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_names = None
        self.load_model()

    def load_model(self, model_name='career_model.joblib', scaler_name='scaler.joblib', encoder_name='label_encoder.joblib'):
        """
        Load model, scaler, and label encoder from disk.
        
        Args:
            model_name: Name of the model file
            scaler_name: Name of the scaler file
            encoder_name: Name of the label encoder file
        """
        model_path = os.path.join(self.model_dir, model_name)
        scaler_path = os.path.join(self.model_dir, scaler_name)
        encoder_path = os.path.join(self.model_dir, encoder_name)
        
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.label_encoder = joblib.load(encoder_path)
            # Try to load saved feature names (list) created during training
            feature_names_path = os.path.join(self.model_dir, 'feature_names.joblib')
            if os.path.exists(feature_names_path):
                self.feature_names = joblib.load(feature_names_path)
            else:
                # Fallback to model's feature_names_in_ if available
                self.feature_names = self.model.feature_names_in_.tolist() if hasattr(self.model, 'feature_names_in_') else None

            logger.info(f"Model loaded successfully from {model_path}")
            if self.feature_names:
                logger.info(f"Loaded feature names: {self.feature_names}")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Model files not found in {self.model_dir}: {e}")

    def predict_career(self, features: np.ndarray) -> Tuple[str, float]:
        """
        Predict single career for given features.
        
        Args:
            features: Array of feature values
            
        Returns:
            Tuple of (predicted_career, confidence)
        """
        if self.model is None:
            raise ValueError("Model not loaded!")
        
        # Normalize features using DataFrame with proper columns if available
        if hasattr(self, 'feature_names') and self.feature_names:
            df = pd.DataFrame([features], columns=self.feature_names)
            features_scaled = self.scaler.transform(df)
        else:
            features_scaled = self.scaler.transform([features])

        # Get prediction and probabilities
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        logger.debug(f"Predictor input features (raw): {features}")
        logger.debug(f"Predictor features (scaled): {features_scaled[0]}")
        logger.debug(f"Predictor probabilities: {probabilities}")
        
        # Get confidence (max probability)
        confidence = float(np.max(probabilities))
        
        return prediction, confidence

    def predict_top_careers(self, features: np.ndarray, top_n: int = 5) -> List[Dict]:
        """
        Get top N career recommendations with compatibility scores.
        
        Args:
            features: Array of feature values (raw, will be scaled)
            top_n: Number of top recommendations to return
            
        Returns:
            List of dicts with career, compatibility_score, and rank
        """
        if self.model is None:
            raise ValueError("Model not loaded!")
        
        # Normalize features using DataFrame with the same feature names used in training
        if hasattr(self, 'feature_names') and self.feature_names:
            df = pd.DataFrame([features], columns=self.feature_names)
            features_scaled = self.scaler.transform(df)
        else:
            features_scaled = self.scaler.transform([features])

        # Get all probabilities from the trained model
        probabilities = self.model.predict_proba(features_scaled)[0]
        class_names = self.label_encoder.classes_
        
        logger.debug("=== DEBUG: Model Prediction ===")
        logger.debug(f"Raw features: {features}")
        logger.debug(f"Scaled features: {features_scaled[0]}")
        logger.debug(f"Probabilities shape: {probabilities.shape}")
        logger.debug(f"Classes: {class_names}")
        logger.debug(f"Probabilities: {probabilities}")
        
        # Create results list
        results = []
        for idx, career in enumerate(class_names):
            compatibility = float(probabilities[idx]) * 100
            results.append({
                'career': career,
                'compatibility_score': round(compatibility, 2),
                'probability': float(probabilities[idx])
            })
        
        # Sort by compatibility score descending
        results = sorted(results, key=lambda x: x['compatibility_score'], reverse=True)
        
        # Return top N
        top_results = results[:top_n]
        print(f"Top {top_n} recommendations: {[r['career'] for r in top_results]}\n")
        
        return top_results

    def get_feature_names(self) -> List[str]:
        """
        Get list of expected feature names.
        
        Returns:
            List of feature names
        """
        if self.model is None:
            raise ValueError("Model not loaded!")
        
        return self.feature_names if self.feature_names else (self.model.feature_names_in_.tolist() if hasattr(self.model, 'feature_names_in_') else [])

    def get_all_careers(self) -> List[str]:
        """
        Get list of all possible career recommendations.
        
        Returns:
            Sorted list of career names
        """
        if self.label_encoder is None:
            raise ValueError("Label encoder not loaded!")
        
        return sorted(self.label_encoder.classes_.tolist())


# Explanation mappings for career compatibility
CAREER_EXPLANATIONS = {
    'Software Developer': {
        'description': 'Develops applications and systems using programming languages.',
        'required_skills': ['Logical thinking', 'Problem-solving', 'Technical knowledge'],
        'suitable_for': 'High logical thinking, strong tech interest, good in math and science.'
    },
    'Data Scientist': {
        'description': 'Analyzes complex data sets to inform business decisions.',
        'required_skills': ['Logical thinking', 'Statistical analysis', 'Programming'],
        'suitable_for': 'Excellent in math and science, strong problem-solving, tech-savvy.'
    },
    'AI/ML Engineer': {
        'description': 'Designs and implements machine learning solutions and AI systems.',
        'required_skills': ['Logical thinking', 'Math', 'Programming', 'Research'],
        'suitable_for': 'High logical/analytical thinking, excellent math, tech interest.'
    },
    'Backend Developer': {
        'description': 'Builds server-side logic and database structures for applications.',
        'required_skills': ['Programming', 'System design', 'Database management'],
        'suitable_for': 'Strong logical thinking, independent work style, tech interest.'
    },
    'Systems Architect': {
        'description': 'Designs large-scale IT systems and infrastructure solutions.',
        'required_skills': ['System design', 'Logical thinking', 'Technical depth'],
        'suitable_for': 'Excellent logical thinking, deep technical knowledge, problem-solving.'
    },
    'Graphic Designer': {
        'description': 'Creates visual content for digital and print media.',
        'required_skills': ['Creativity', 'Visual design', 'Artistic ability'],
        'suitable_for': 'High creativity, good art scores, visual thinking ability.'
    },
    'UX Designer': {
        'description': 'Designs user interfaces and experiences for digital products.',
        'required_skills': ['Creativity', 'User empathy', 'Problem-solving'],
        'suitable_for': 'Balanced creativity and logic, good communication, user-focused.'
    },
    'Product Manager': {
        'description': 'Leads the development and strategy of digital products.',
        'required_skills': ['Leadership', 'Communication', 'Strategic thinking'],
        'suitable_for': 'Strong communication and leadership, balanced skills, collaborative.'
    },
    'Business Manager': {
        'description': 'Oversees business operations and team management.',
        'required_skills': ['Leadership', 'Communication', 'Problem-solving'],
        'suitable_for': 'Excellent communication, leadership aptitude, collaborative style.'
    },
    'Project Manager': {
        'description': 'Manages projects from planning to completion and delivery.',
        'required_skills': ['Organization', 'Communication', 'Leadership'],
        'suitable_for': 'Good communication, organizational skills, team collaboration.'
    },
    'HR Manager': {
        'description': 'Manages human resources, recruitment, and employee relations.',
        'required_skills': ['Communication', 'Empathy', 'Leadership'],
        'suitable_for': 'Excellent communication, people skills, collaborative approach.'
    },
    'Sales Manager': {
        'description': 'Leads sales teams and manages customer relationships.',
        'required_skills': ['Communication', 'Leadership', 'Persuasion'],
        'suitable_for': 'Strong communication and leadership, collaborative, people-oriented.'
    },
    'Consultant': {
        'description': 'Provides expert advice to organizations on business challenges.',
        'required_skills': ['Analytical thinking', 'Communication', 'Leadership'],
        'suitable_for': 'Strong analysis and communication, problem-solving, collaborative.'
    },
    'Digital Marketer': {
        'description': 'Manages digital marketing campaigns and online presence.',
        'required_skills': ['Creativity', 'Analysis', 'Communication'],
        'suitable_for': 'Creative thinking, good communication, balanced tech interest.'
    },
    'Content Creator': {
        'description': 'Creates engaging content across various digital platforms.',
        'required_skills': ['Creativity', 'Communication', 'Storytelling'],
        'suitable_for': 'High creativity, strong communication, social interest.'
    },
    'Social Media Manager': {
        'description': 'Manages social media presence and community engagement.',
        'required_skills': ['Communication', 'Creativity', 'Social skills'],
        'suitable_for': 'Strong communication and social skills, creative, people-focused.'
    },
    'Brand Manager': {
        'description': 'Develops and manages brand strategy and identity.',
        'required_skills': ['Creativity', 'Communication', 'Strategic thinking'],
        'suitable_for': 'Creative, good communication, strategic thinking, collaborative.'
    }
}


def get_career_explanation(career: str) -> Dict:
    """
    Get explanation details for a specific career.
    
    Args:
        career: Career name
        
    Returns:
        Dict with career information or default message
    """
    return CAREER_EXPLANATIONS.get(career, {
        'description': f'{career} is a professional path that matches your profile.',
        'required_skills': ['Problem-solving', 'Continuous learning'],
        'suitable_for': 'Your demonstrated abilities and interests.'
    })
