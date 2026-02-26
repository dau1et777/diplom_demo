"""
Test script for the ability-based recommendation system
Tests the full pipeline: import careers -> cluster -> recommend
"""
import os
import sys
import django

# Setup Django from backend directory
backend_dir = r'c:\Users\konra\diplomka\backend'
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.careers.models import Career
from ml.ability_recommender import AbilityRecommendationService, ABILITY_NAMES
import numpy as np


def test_ability_recommender():
    """Test the ability-based recommendation system."""
    print("\n" + "=" * 80)
    print("ABILITY-BASED RECOMMENDATION SYSTEM - TEST")
    print("=" * 80)
    
    # Check career count
    career_count = Career.objects.count()
    print(f"\n[1/5] Career Database Status:")
    print(f"  ✓ Total careers in database: {career_count}")
    
    if career_count < 10:
        print(f"  ⚠ Warning: Only {career_count} careers. Need to import 80+")
        return False
    
    # Analyze clusters
    clusters = Career.objects.values_list('cluster', flat=True).distinct()
    print(f"\n[2/5] Cluster Distribution:")
    for cluster in sorted(clusters):
        count = Career.objects.filter(cluster=cluster).count()
        print(f"  ✓ {cluster}: {count} careers")
    
    # Initialize service
    print(f"\n[3/5] Initializing AbilityRecommendationService...")
    service = AbilityRecommendationService()
    print(f"  ✓ Service initialized")
    print(f"  ✓ Ability dimensions: {len(ABILITY_NAMES)}")
    for i, name in enumerate(ABILITY_NAMES):
        print(f"     {i}: {name}")
    
    # Test with sample tech-focused student
    print(f"\n[4/5] Testing with Tech-Focused Student Profile:")
    quiz_answers = {
        "logical_thinking": 9,
        "analytical_skills": 8,
        "mathematical_ability": 8,
        "problem_solving": 9,
        "creativity": 6,
        "technical_skills": 10,
        "programming": 10,
        "communication": 6,
        "leadership": 5,
        "teamwork": 6,
    }
    
    # Extract abilities
    user_abilities = service.extract_user_abilities(quiz_answers)
    print(f"  ✓ User ability profile extracted:")
    for i, (name, value) in enumerate(zip(ABILITY_NAMES, user_abilities)):
        print(f"     {name}: {value:.1f}/10")
    
    # Get recommendations
    print(f"\n[5/5] Generating Top-5 Recommendations:")
    recommendations = service.recommend(quiz_answers, top_n=5, diversity=True)
    
    if not recommendations:
        print(f"  ✗ No recommendations generated!")
        return False
    
    for idx, rec in enumerate(recommendations, 1):
        print(f"\n  #{idx}. {rec.career.name}")
        print(f"      Match Score: {rec.match_score * 100:.1f}%")
        print(f"      Coverage: {rec.coverage_score * 100:.1f}%")
        print(f"      Cluster: {rec.career.cluster}")
        print(f"      Top Abilities: {', '.join(rec.top_matching_abilities) if rec.top_matching_abilities else 'None'}")
        print(f"      Missing Abilities: {', '.join(rec.missing_abilities) if rec.missing_abilities else 'None'}")
        print(f"      Salary: {rec.salary_range}")
    
    # Test with creative student
    print(f"\n" + "=" * 80)
    print("Testing with Creative-Focused Student Profile:")
    quiz_answers_creative = {
        "creativity": 9,
        "artistic_ability": 9,
        "communication": 8,
        "leadership": 7,
        "interpersonal_skills": 8,
        "logical_thinking": 5,
        "mathematical_ability": 4,
        "technical_skills": 3,
    }
    
    recs_creative = service.recommend(quiz_answers_creative, top_n=5, diversity=True)
    
    print(f"\nTop-5 Creative Recommendations:")
    for idx, rec in enumerate(recs_creative, 1):
        print(f"  #{idx}. {rec.career.name} ({rec.career.cluster}) - {rec.match_score * 100:.1f}%")
    
    print(f"\n" + "=" * 80)
    print("✓ ALL TESTS COMPLETED")
    print("=" * 80 + "\n")
    
    return True


if __name__ == '__main__':
    success = test_ability_recommender()
    sys.exit(0 if success else 1)
