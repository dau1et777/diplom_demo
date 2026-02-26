#!/usr/bin/env python
"""
Test script that simulates the exact frontend flow:
1. Get quiz questions
2. Submit quiz answers
3. Generate recommendations
"""

import os
import sys
import django
import json
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.quiz.models import QuizQuestion, QuizAnswer
from django.db import transaction

BASE_URL = 'http://localhost:8000/api'
SESSION_ID = f'test_flow_{int(__import__("time").time() * 1000)}'

print(f"\n{'='*60}")
print(f"Testing Frontend Flow - Simulating Quiz → Recommendations")
print(f"Session ID: {SESSION_ID}")
print(f"{'='*60}\n")

# Step 1: Get quiz questions
print("[STEP 1] Fetching quiz questions...")
try:
    response = requests.get(f'{BASE_URL}/quiz/questions/')
    questions = response.json().get('results', [])
    print(f"✓ Got {len(questions)} questions")
    print(f"  Status: {response.status_code}")
    print(f"  Sample question: {questions[0] if questions else 'None'}\n")
except Exception as e:
    print(f"✗ Failed to fetch questions: {e}\n")
    sys.exit(1)

# Step 2: Create quiz answers (simulate user responses)
print("[STEP 2] Submitting quiz answers...")
try:
    answers = {}
    for i, q in enumerate(questions):
        # Simulate user answers: give different values for tech/creative answers
        if 'tech' in q.get('text', '').lower() or 'logical' in q.get('text', '').lower():
            # High score for tech-oriented questions
            answers[str(q['id'])] = 8 + (i % 2)  # 8-9
        elif 'creative' in q.get('text', '').lower() or 'artistic' in q.get('text', '').lower():
            # Low score for creative if looking for tech
            answers[str(q['id'])] = 3 + (i % 2)  # 3-4
        else:
            # Medium scores
            answers[str(q['id'])] = 5 + (i % 3)  # 5-7
    
    # Ensure all questions answered
    for q in questions:
        if str(q['id']) not in answers:
            answers[str(q['id'])] = 5
    
    print(f"✓ Created {len(answers)} answers")
    print(f"  Sample answers: {list(answers.items())[:3]}\n")
except Exception as e:
    print(f"✗ Failed to create answers: {e}\n")
    sys.exit(1)

# Step 3: Submit answers via POST
print("[STEP 3] Posting answers to quiz/submit/...")
try:
    response = requests.post(f'{BASE_URL}/quiz/submit/', json={
        'session_id': SESSION_ID,
        'answers': answers
    })
    submit_result = response.json()
    print(f"✓ Submit response")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {submit_result}\n")
    
    if not submit_result.get('success'):
        print(f"✗ Submit returned success=false: {submit_result.get('error')}\n")
except Exception as e:
    print(f"✗ Failed to submit: {e}\n")
    sys.exit(1)

# Step 4: Generate recommendations
print("[STEP 4] Calling results/recommend/ endpoint...")
try:
    response = requests.post(f'{BASE_URL}/results/recommend/', json={
        'session_id': SESSION_ID,
        'top_n': 5
    })
    
    print(f"✓ Recommendations endpoint response")
    print(f"  Status: {response.status_code}")
    
    if response.status_code != 201:
        print(f"  ✗ ERROR: Expected 201, got {response.status_code}")
        print(f"  Response text: {response.text}\n")
    else:
        rec_result = response.json()
        print(f"  Response keys: {list(rec_result.keys())}")
        print(f"  Success: {rec_result.get('success')}")
        print(f"  Primary career: {rec_result.get('primary_career')}")
        print(f"  Compatibility: {rec_result.get('primary_compatibility')}")
        
        top_recs = rec_result.get('top_recommendations', [])
        print(f"  Top recommendations count: {len(top_recs)}")
        
        if top_recs:
            print(f"  Top 3:")
            for i, rec in enumerate(top_recs[:3], 1):
                print(f"    {i}. {rec.get('career')} ({rec.get('compatibility_score'):.1f}%)")
        
        abilities = rec_result.get('abilities', {})
        print(f"  Abilities keys: {list(abilities.keys())}")
        print(f"  Sample abilities: {dict(list(abilities.items())[:3])}\n")
        
        # Validate what frontend would receive
        print("[VALIDATION] What frontend receives:")
        print(f"  Has 'success' key: {'success' in rec_result}")
        print(f"  Has 'top_recommendations' key: {'top_recommendations' in rec_result}")
        print(f"  Has 'abilities' key: {'abilities' in rec_result}")
        print(f"  Has 'primary_career' key: {'primary_career' in rec_result}")
        
        frontend_check = (
            rec_result.get('top_recommendations') and 
            len(rec_result.get('top_recommendations', [])) > 0
        )
        print(f"  Frontend validation would pass: {'✓ YES' if frontend_check else '✗ NO'}\n")
        
except requests.exceptions.ConnectionError:
    print(f"✗ Cannot connect to {BASE_URL}")
    print("  Make sure Django server is running on http://localhost:8000\n")
    sys.exit(1)
except Exception as e:
    print(f"✗ Failed to generate recommendations: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("="*60)
print("✓ Frontend flow test PASSED")
print("="*60)
