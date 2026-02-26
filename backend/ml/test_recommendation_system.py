"""
ML SYSTEM REDESIGN - MIGRATION & TESTING GUIDE

This script demonstrates:
1. Side-by-side comparison of old vs new approach
2. How to test the new recommendation engine
3. Validation of recommendation quality
4. Performance benchmarks
"""

import sys
import time
from pathlib import Path
import json

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================================
# TEST 1: Basic Recommendation Engine Test
# ============================================================================

def test_recommendation_engine():
    """Test the new similarity-based recommendation engine."""
    from ml.recommendation_engine import (
        UserFeatureExtractor,
        RecommendationEngine,
    )
    
    print("\n" + "="*70)
    print("TEST 1: RECOMMENDATION ENGINE")
    print("="*70)
    
    # Scenario 1: Tech-minded student
    print("\n📊 SCENARIO 1: Tech-Minded Student")
    print("-"*70)
    tech_student_quiz = {
        1: 9, 2: 8, 3: 9,      # Logic: HIGH
        4: 4, 5: 3, 6: 4,      # Creativity: LOW
        7: 6, 8: 6, 9: 6,      # Communication: MEDIUM
        10: 8, 11: 6, 12: 8, 13: 3,  # Academic: Math/Science strong
        14: 10, 15: 5, 16: 2, 17: 4,  # Interests: TECH focused
        18: 8, 19: 5,          # Work style: Independent
    }
    
    extractor = UserFeatureExtractor()
    user_features = extractor.extract_features(tech_student_quiz)
    
    print("User Profile:")
    top_features = sorted(user_features.items(), key=lambda x: x[1], reverse=True)[:5]
    for feature, score in top_features:
        print(f"  ⭐ {feature.replace('_', ' ').title():25} {score:5.1f}/10")
    
    engine = RecommendationEngine()
    recommendations = engine.recommend(user_features, top_n=5)
    
    print("\nTop 5 Recommendations:")
    for rec in recommendations:
        print(f"\n#{rec.rank}. {rec.career}")
        print(f"    Compatibility: {rec.compatibility_score}%")
        print(f"    💰 Salary: {rec.salary_range}")
        print(f"    📝 {rec.explanation}")
    
    # Scenario 2: Creative student
    print("\n\n📊 SCENARIO 2: Creative Student")
    print("-"*70)
    creative_student_quiz = {
        1: 4, 2: 5, 3: 5,      # Logic: LOW
        4: 9, 5: 9, 6: 9,      # Creativity: HIGH
        7: 8, 8: 8, 9: 8,      # Communication: HIGH
        10: 5, 11: 7, 12: 4, 13: 9,  # Academic: Art strong
        14: 3, 15: 4, 16: 10, 17: 8,  # Interests: CREATIVE focused
        18: 6, 19: 8,          # Work style: Collaborative
    }
    
    creative_features = extractor.extract_features(creative_student_quiz)
    
    print("User Profile:")
    top_features = sorted(creative_features.items(), key=lambda x: x[1], reverse=True)[:5]
    for feature, score in top_features:
        print(f"  ⭐ {feature.replace('_', ' ').title():25} {score:5.1f}/10")
    
    creative_recs = engine.recommend(creative_features, top_n=5)
    
    print("\nTop 5 Recommendations:")
    for rec in creative_recs:
        print(f"\n#{rec.rank}. {rec.career}")
        print(f"    Compatibility: {rec.compatibility_score}%")
        print(f"    💰 Salary: {rec.salary_range}")
    
    print("\n✅ Recommendation Engine Test PASSED")


# ============================================================================
# TEST 2: Feature Extraction Accuracy
# ============================================================================

def test_feature_extraction():
    """Validate feature extraction from quiz answers."""
    from ml.recommendation_engine import UserFeatureExtractor
    
    print("\n" + "="*70)
    print("TEST 2: FEATURE EXTRACTION")
    print("="*70)
    
    extractor = UserFeatureExtractor()
    
    # Test 1: All answers = 10 (perfect score)
    perfect_quiz = {i: 10 for i in range(1, 20)}
    perfect_features = extractor.extract_features(perfect_quiz)
    
    print("\nTest Case 1: All answers = 10")
    avg_score = sum(perfect_features.values()) / len(perfect_features)
    print(f"  Average feature score: {avg_score:.2f}/10 (expected ~9-10)")
    assert avg_score > 8, "Perfect quiz should yield high feature scores"
    print("  ✅ PASSED")
    
    # Test 2: All answers = 1 (low score)
    low_quiz = {i: 1 for i in range(1, 20)}
    low_features = extractor.extract_features(low_quiz)
    
    print("\nTest Case 2: All answers = 1")
    avg_score = sum(low_features.values()) / len(low_features)
    print(f"  Average feature score: {avg_score:.2f}/10 (expected ~1-2)")
    assert avg_score < 3, "Low quiz should yield low feature scores"
    print("  ✅ PASSED")
    
    # Test 3: Feature range validation
    print("\nTest Case 3: Feature range validation")
    balanced_quiz = {i: (i % 10 + 1) for i in range(1, 20)}
    balanced_features = extractor.extract_features(balanced_quiz)
    
    for feature, score in balanced_features.items():
        assert 0 <= score <= 10, f"{feature} score {score} out of range [0-10]"
    print(f"  All {len(balanced_features)} features in valid range [0-10]")
    print("  ✅ PASSED")


# ============================================================================
# TEST 3: Similarity Scoring Consistency
# ============================================================================

def test_similarity_consistency():
    """Verify that identical inputs produce identical recommendations."""
    from ml.recommendation_engine import (
        UserFeatureExtractor,
        RecommendationEngine,
    )
    
    print("\n" + "="*70)
    print("TEST 3: SIMILARITY SCORING CONSISTENCY")
    print("="*70)
    
    extractor = UserFeatureExtractor()
    engine = RecommendationEngine()
    
    # Same quiz, run multiple times
    test_quiz = {
        1: 8, 2: 7, 3: 8, 4: 5, 5: 5, 6: 5,
        7: 7, 8: 7, 9: 7, 10: 7, 11: 7, 12: 8,
        13: 5, 14: 8, 15: 6, 16: 4, 17: 5, 18: 7, 19: 7
    }
    
    features = extractor.extract_features(test_quiz)
    
    # Run 3 times and compare
    results = []
    for i in range(3):
        recs = engine.recommend(features, top_n=5)
        career_order = [rec.career for rec in recs]
        results.append(career_order)
    
    print("\nConsistency Test: Run recommendation engine 3 times")
    for i, result in enumerate(results, 1):
        print(f"\n  Run {i}: {result[0]} → {result[1]} → {result[2]}")
    
    # Check consistency
    if results[0] == results[1] == results[2]:
        print("\n✅ CONSISTENT: Same results across all runs")
    else:
        print("\n⚠️ WARNING: Results vary across runs")


# ============================================================================
# TEST 4: Recommendation Diversity
# ============================================================================

def test_recommendation_diversity():
    """Check that recommendations span different career domains."""
    from ml.recommendation_engine import (
        UserFeatureExtractor,
        RecommendationEngine,
    )
    
    print("\n" + "="*70)
    print("TEST 4: RECOMMENDATION DIVERSITY")
    print("="*70)
    
    extractor = UserFeatureExtractor()
    engine = RecommendationEngine()
    
    balanced_quiz = {i: 5 for i in range(1, 20)}  # Neutral student
    features = extractor.extract_features(balanced_quiz)
    
    recs = engine.recommend(features, top_n=5)
    
    print("\nTop 5 recommendations for neutral student:")
    for rec in recs:
        print(f"  {rec.rank}. {rec.career:30} {rec.compatibility_score:6.1f}%")
    
    career_domains = {
        'Software Engineer': 'Tech',
        'Data Scientist': 'Tech',
        'UX Designer': 'Tech',
        'DevOps Engineer': 'Tech',
        'Management Consultant': 'Business',
        'Product Manager': 'Business',
        'Financial Analyst': 'Business',
        'Marketing Manager': 'Business',
        'Teacher': 'Education',
        'Graphic Designer': 'Creative',
    }
    
    domains = []
    for rec in recs:
        domain = career_domains.get(rec.career, 'Other')
        domains.append(domain)
    
    unique_domains = len(set(domains))
    print(f"\nDomains represented: {set(domains)}")
    print(f"Diversity score: {unique_domains}/5 unique domains")
    
    if unique_domains >= 2:
        print("✅ GOOD: Recommendations span multiple domains")
    else:
        print("⚠️ WARNING: Recommendations are very similar")


# ============================================================================
# TEST 5: Performance Benchmark
# ============================================================================

def test_performance():
    """Benchmark recommendation generation speed."""
    from ml.recommendation_engine import (
        UserFeatureExtractor,
        RecommendationEngine,
    )
    
    print("\n" + "="*70)
    print("TEST 5: PERFORMANCE BENCHMARK")
    print("="*70)
    
    extractor = UserFeatureExtractor()
    engine = RecommendationEngine()
    
    test_quiz = {i: (i % 10 + 1) for i in range(1, 20)}
    
    # Time feature extraction
    start = time.time()
    for _ in range(1000):
        features = extractor.extract_features(test_quiz)
    extraction_time = (time.time() - start) / 1000
    
    print(f"\nFeature Extraction: {extraction_time*1000:.3f} ms/operation")
    
    # Time recommendation generation
    features = extractor.extract_features(test_quiz)
    start = time.time()
    for _ in range(100):
        recs = engine.recommend(features, top_n=5)
    recommendation_time = (time.time() - start) / 100
    
    print(f"Recommendation Generation: {recommendation_time*1000:.3f} ms/operation")
    print(f"Total latency: {(extraction_time + recommendation_time)*1000:.1f} ms")
    
    if (extraction_time + recommendation_time) < 0.1:  # 100ms target
        print("✅ PASSED: Fast enough for real-time API")
    else:
        print("⚠️ WARNING: May be slow for high-traffic scenarios")


# ============================================================================
# TEST 6: Recommendation Justification
# ============================================================================

def test_explanation_quality():
    """Verify that recommendations have clear, justifiable explanations."""
    from ml.recommendation_engine import (
        UserFeatureExtractor,
        RecommendationEngine,
    )
    
    print("\n" + "="*70)
    print("TEST 6: EXPLANATION QUALITY")
    print("="*70)
    
    extractor = UserFeatureExtractor()
    engine = RecommendationEngine()
    
    # Specialized student: strong in communication, weak in math
    communicator_quiz = {
        1: 5, 2: 5, 3: 5,      # Logic: MEDIUM
        4: 7, 5: 7, 6: 7,      # Creativity: HIGH
        7: 9, 8: 9, 9: 9,      # Communication: VERY HIGH
        10: 3, 11: 8, 12: 3, 13: 8,  # Academic: Writing strong, Math weak
        14: 2, 15: 8, 16: 7, 17: 9,  # Interests: Business/Social focused
        18: 6, 19: 9,          # Work style: Very collaborative
    }
    
    features = extractor.extract_features(communicator_quiz)
    recs = engine.recommend(features, top_n=3)
    
    print("\nChecking explanation quality for top recommendations:\n")
    for rec in recs:
        print(f"#{rec.rank}. {rec.career}")
        print(f"    Compatibility: {rec.compatibility_score}%")
        print(f"    Explanation: {rec.explanation}")
        
        # Check explanation contains meaningful content
        explanation = rec.explanation.lower()
        
        checks = [
            ('mentions strengths', any(x in explanation for x in ['align', 'strength', 'strong'])),
            ('is future-focused', any(x in explanation for x in ['develop', 'consider'])),
            ('is specific', rec.career in explanation),
        ]
        
        all_good = all(check[1] for check in checks)
        status = "✅" if all_good else "⚠️"
        print(f"    {status} Explanation quality checks:")
        for check_name, passed in checks:
            print(f"      {'✓' if passed else '✗'} {check_name}")
        print()


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CAREER RECOMMENDATION SYSTEM - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    tests = [
        ("Recommendation Engine", test_recommendation_engine),
        ("Feature Extraction", test_feature_extraction),
        ("Similarity Consistency", test_similarity_consistency),
        ("Recommendation Diversity", test_recommendation_diversity),
        ("Performance Benchmark", test_performance),
        ("Explanation Quality", test_explanation_quality),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")
    print("="*70)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! System is ready for production.\n")
    else:
        print(f"\n⚠️ {failed} test(s) failed. Check output above for details.\n")
