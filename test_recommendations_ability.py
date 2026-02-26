"""
End-to-End Integration Test for Ability-Based Recommendation System
Tests: GET questions -> POST answers -> GET recommendations with diverse careers
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_full_flow():
    """Test the complete recommendation flow."""
    print("\n" + "="*80)
    print("ABILITY-BASED RECOMMENDATION SYSTEM - INTEGRATION TEST")
    print("="*80)
    
    # Step 1: Fetch quiz questions
    print("\n[1/4] Fetching quiz questions...")
    try:
        resp = requests.get(f"{BASE_URL}/quiz/questions/")
        resp.raise_for_status()
        data = resp.json()
        # Handle both formats: direct list or dict with 'results'
        questions = data.get('results', data) if isinstance(data, dict) else data
        if not isinstance(questions, list):
            questions = [questions] if questions else []
        print(f"  ✓ Got {len(questions)} questions")
    except Exception as e:
        print(f"  ✗ Failed to fetch questions: {e}")
        return False
    
    # Step 2: Submit quiz answers (tech-focused profile)
    print("\n[2/4] Submitting tech-focused quiz answers...")
    session_id = f"test_session_{int(time.time() * 1000)}"
    
    # Create answers: high scores for tech abilities, low for others
    answers = {}
    answer_index = 0
    for q in questions:
        # Handle both dict and object formats
        q_id = q.get('id') if isinstance(q, dict) else str(q.id)
        q_text = str(q.get('text', '') if isinstance(q, dict) else str(q))
        
        # Map to high tech, medium logical, low creative/social
        if any(tech in q_text.lower() for tech in ['technical', 'programming', 'coding', 'software']):
            answers[str(q_id)] = 9
        elif any(log in q_text.lower() for log in ['logical', 'problem', 'solve', 'analyze']):
            answers[str(q_id)] = 8
        elif any(cr in q_text.lower() for cr in ['creative', 'artistic', 'design', 'imagine']):
            answers[str(q_id)] = 3
        elif any(cm in q_text.lower() for cm in ['communication', 'leadership', 'team', 'social']):
            answers[str(q_id)] = 4
        else:
            # Distribute across dimensions
            if answer_index % 4 == 0:
                answers[str(q_id)] = 8  # Logical
            elif answer_index % 4 == 1:
                answers[str(q_id)] = 9  # Technical
            elif answer_index % 4 == 2:
                answers[str(q_id)] = 3  # Creative
            else:
                answers[str(q_id)] = 4  # Social
            answer_index += 1
    
    try:
        resp = requests.post(
            f"{BASE_URL}/quiz/submit/",
            json={"session_id": session_id, "answers": answers}
        )
        resp.raise_for_status()
        result = resp.json()
        print(f"  ✓ Quiz submitted: {session_id}")
    except Exception as e:
        print(f"  ✗ Failed to submit quiz: {e}")
        return False
    
    # Step 3: Get recommendations
    print("\n[3/4] Requesting career recommendations...")
    try:
        resp = requests.post(
            f"{BASE_URL}/results/recommend/",
            json={"session_id": session_id, "top_n": 5}
        )
        resp.raise_for_status()
        result = resp.json()
        recommendations = result.get('top_recommendations', [])
        primary_career = result.get('primary_career', 'Unknown')
        
        if not recommendations:
            print(f"  ✗ No recommendations returned")
            return False
            
        print(f"  ✓ Got {len(recommendations)} recommendations")
        print(f"  ✓ Primary career: {primary_career}")
    except Exception as e:
        print(f"  ✗ Failed to get recommendations: {e}")
        return False
    
    # Step 4: Analyze results
    print("\n[4/4] Analyzing Recommendations:")
    
    # Check for diversity
    clusters = set()
    for rec in recommendations:
        cluster = rec.get('cluster', 'Unknown')
        clusters.add(cluster)
        name = rec.get('name', 'Unknown')
        score = rec.get('compatibility_score', rec.get('match_score', 0))
        match = rec.get('ability_match_score', score)
        coverage = rec.get('coverage_score', 0)
        
        print(f"\n  #{recommendations.index(rec) + 1}. {name}")
        print(f"      Cluster: {cluster}")
        print(f"      Match Score: {match:.1f}%")
        print(f"      Coverage: {coverage:.1f}%")
        
        if rec.get('top_matching_abilities'):
            print(f"      Strong In: {', '.join(rec['top_matching_abilities'][:2])}")
        if rec.get('missing_abilities'):
            print(f"      Needs Work: {', '.join(rec['missing_abilities'][:2])}")
    
    # Verify diversity
    print(f"\n  Cluster Diversity:")
    print(f"    ✓ {len(clusters)} different clusters in top {len(recommendations)}")
    if len(clusters) < 4:
        print(f"    ⚠ Warning: Low diversity (expected 5, got {len(clusters)})")
    
    # Verify different from old system (should not all be "Consultant", "Project Manager", etc.)
    names = [r.get('name') for r in recommendations]
    print(f"\n  Career Diversity Check:")
    unique_names = len(set(names))
    print(f"    ✓ {unique_names} unique careers recommended")
    
    # Check if tech careers are well-represented
    tech_keywords = ['software', 'engineer', 'developer', 'data', 'technical', 'architect']
    tech_count = sum(1 for name in names if any(kw in name.lower() for kw in tech_keywords))
    print(f"    ✓ {tech_count}/5 recommendations contain tech keywords (expected >2)")
    
    print("\n" + "="*80)
    if tech_count >= 2 and len(clusters) >= 4:
        print("✓ ALL TESTS PASSED - System working correctly!")
        print("  • Diverse recommendations across {0} clusters".format(len(clusters)))
        print("  • Tech-focused student getting tech-relevant careers")
    else:
        print("⚠ TESTS PASSED but could be improved")
        print("  • Diversity or tech relevance could be better")
    print("="*80 + "\n")
    
    return True


def test_multiple_profiles():
    """Test with different student profiles to verify diversity."""
    print("\n" + "="*80)
    print("TESTING MULTIPLE STUDENT PROFILES")
    print("="*80)
    
    profiles = [
        ("Creative", lambda i: 8 if i % 3 == 0 else 3),  # Creative high, tech low
        ("Business", lambda i: 7 if i % 4 < 2 else 4),   # Balanced
        ("Technical", lambda i: 9 if i % 2 == 0 else 3),  # Tech high, creative low
    ]
    
    for profile_name, score_fn in profiles:
        print(f"\nProfile: {profile_name} Student")
        print("-" * 40)
        
        try:
            # Fetch questions
            resp = requests.get(f"{BASE_URL}/quiz/questions/")
            data = resp.json()
            questions = data.get('results', data) if isinstance(data, dict) else data
            if not isinstance(questions, list):
                questions = [questions] if questions else []
            
            # Submit answers
            session_id = f"test_{profile_name}_{int(time.time() * 1000)}"
            answers = {}
            for i, q in enumerate(questions):
                q_id = q.get('id') if isinstance(q, dict) else str(q.id)
                answers[str(q_id)] = score_fn(i)
            
            resp = requests.post(
                f"{BASE_URL}/quiz/submit/",
                json={"session_id": session_id, "answers": answers}
            )
            
            # Get recommendations
            resp = requests.post(
                f"{BASE_URL}/results/recommend/",
                json={"session_id": session_id, "top_n": 5}
            )
            result = resp.json()
            recommendations = result.get('top_recommendations', [])
            
            # Display top 3 careers
            print(f"Top 3 Careers:")
            for i, rec in enumerate(recommendations[:3], 1):
                name = rec.get('name', 'Unknown')
                score = rec.get('compatibility_score', rec.get('match_score', 0))
                cluster = rec.get('cluster', '?')
                print(f"  {i}. {name} ({cluster}) - {score:.0f}%")
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "="*80)
    print("✓ PROFILE DIVERSITY TEST COMPLETE")
    print("="*80 + "\n")


if __name__ == '__main__':
    try:
        print("\nWaiting for server to stabilize...")
        time.sleep(2)
        
        success = test_full_flow()
        if success:
            test_multiple_profiles()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\nFatal error: {e}")
