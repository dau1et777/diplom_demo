#!/usr/bin/env python
"""
Test script to verify the career recommendations endpoint works.
This tests the fallback behavior when HybridRecommendationService is unavailable.
"""

import requests
import json
import os

API_URL = "http://localhost:8000/api"
# cache file for question ids to avoid repeated network calls
CACHE_FILE = os.path.join(os.path.dirname(__file__), 'question_ids_cache.json')

# single session to reuse connection headers
session = requests.Session()

def test_recommendations():
    """Test the entire quiz -> recommendations flow."""
    
    print("=" * 70)
    print("CAREER RECOMMENDATION SYSTEM - INTEGRATION TEST")
    print("=" * 70)
    
    # Step 1: Get quiz questions
    print("\n[1/4] Fetching quiz questions (with cache)...")
    questions = []
    if os.path.exists(CACHE_FILE):
        try:
            questions = json.load(open(CACHE_FILE))
            print(f"✓ Loaded {len(questions)} questions from cache")
        except Exception as e:
            print(f"⚠ Failed to load cache: {e}, will fetch from backend")
    if not questions:
        try:
            response = session.get(f"{API_URL}/quiz/questions/")
            response.raise_for_status()
            questions = response.json().get('results', [])
            print(f"✓ Got {len(questions)} questions from backend")
            with open(CACHE_FILE, 'w') as f:
                json.dump(questions, f)
        except Exception as e:
            print(f"✗ Failed to fetch questions: {e}")
            return False
    
    # Step 2: Submit quiz answers with tech-focused profile
    print("\n[2/4] Submitting quiz answers (tech-focused profile)...")
    session_id = "test_session_" + str(int(__import__('time').time() * 1000))
    
    # Create answers dict - all high scores (simulating tech student)
    answers_dict = {}
    for q in questions:
        answers_dict[str(q['id'])] = 10  # Max score for all questions
    
    try:
        response = session.post(
            f"{API_URL}/quiz/submit/",
            json={"session_id": session_id, "answers": answers_dict}
        )
        response.raise_for_status()
        submission = response.json()
        print(f"✓ Quiz submitted: session_id={session_id}")
    except Exception as e:
        print(f"✗ Failed to submit quiz: {e}")
        return False
    
    # Step 3: Request recommendations
    print("\n[3/4] Requesting career recommendations...")
    try:
        response = session.post(
            f"{API_URL}/results/recommend/",
            json={"session_id": session_id, "top_n": 10}  # Show 10 careers
        )
        if response.status_code not in (200, 201):
            print(f"✗ API returned {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        recommendations = response.json()
        print(f"✓ Got recommendations")
        
        if not recommendations.get('success'):
            print(f"✗ Recommendations failed: {recommendations.get('error')}")
            return False
        
    except Exception as e:
        print(f"✗ Failed to get recommendations: {e}")
        return False
    
    # Step 4: Display results
    print("\n[4/4] Displaying results...")
    print("-" * 70)
    
    top_recs = recommendations.get('top_recommendations', [])
    print(f"\nTop {len(top_recs)} Career Recommendations:\n")
    
    for idx, rec in enumerate(top_recs, 1):
        career = rec.get('career')
        if not career:
            print(f"✗ Recommendation {idx} missing career name: {rec}")
            return False
        # Handle both old (compatibility_score) and new (score) formats
        score = rec.get('score') or rec.get('compatibility_score', 0)
        cluster = rec.get('cluster', 'N/A')
        
        print(f"#{idx}. {career}")
        print(f"   Score: {score}%")
        print(f"   Cluster: {cluster}")
        
        if 'explanation' in rec:
            print(f"   Explanation: {rec['explanation'][:100]}...")
        print()
    
    # Summary
    print("-" * 70)
    abilities = recommendations.get('abilities', {})
    print(f"\nUser Ability Scores: {json.dumps(abilities, indent=2)[:200]}...")

    # Expect interest breakdown present
    for key in ['interest_tech','interest_business','interest_creativity','interest_social']:
        if key not in abilities:
            print(f"✗ Missing interest score '{key}' in abilities")
            return False
    
    # Expect work style present
    for key in ['work_style_independent', 'work_style_collaborative']:
        if key not in abilities:
            print(f"✗ Missing work_style score '{key}' in abilities")
            return False
    
    # Expect core ability scores present
    for key in ['logical_thinking', 'creativity', 'communication', 'problem_solving', 'teamwork', 'leadership']:
        if key not in abilities:
            print(f"✗ Missing core ability score '{key}' in abilities")
            return False

    # Step 5: verify viewCareer endpoint works
    if top_recs:
        first = top_recs[0]
        career_name = first.get('career')
        print(f"\n[5/5] Sending viewCareer event for '{career_name}'...")
        try:
            view_resp = session.post(
                f"{API_URL}/results/view-career/",
                json={"session_id": session_id, "career": career_name}
            )
            if view_resp.status_code not in (200, 201):
                print(f"✗ view_career returned {view_resp.status_code}: {view_resp.text}")
                return False
            print("✓ view_career recorded successfully")
        except Exception as e:
            print(f"✗ view_career request failed: {e}")
            return False
    
    print("\n" + "=" * 70)
    print("✓ ALL TESTS PASSED - System is working!")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    success = test_recommendations()
    exit(0 if success else 1)
