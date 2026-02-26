"""
Test API Response Structure
Simulates frontend API call to backend and verifies response structure
"""
import os
import sys
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from apps.quiz.models import QuizQuestion, QuizAnswer
from apps.results.views import CareerRecommendationViewSet

print("\n" + "="*80)
print("TESTING API RESPONSE STRUCTURE")
print("="*80)

# Create test session ID
session_id = "test_session_12345"
print(f"\nTest Session ID: {session_id}")

# Fetch all questions
all_questions = QuizQuestion.objects.all()
print(f"Total questions in DB: {all_questions.count()}")

# Create quiz answers for this session
print("\nCreating quiz answers in database...")
for question in all_questions:
    if question.category == 'logic':
        response = 9
    elif question.category == 'communication':
        response = 3
    else:
        response = 5
    
    QuizAnswer.objects.create(
        session_id=session_id,
        question=question,
        user_response=response
    )

print(f"✓ Created {QuizAnswer.objects.filter(session_id=session_id).count()} quiz answers")

# Now test the API endpoint using DRF test client
print("\nTesting API endpoint: POST /api/results/recommend/")
print("-" * 80)

client = Client()
response = client.post(
    '/api/results/recommend/',
    data=json.dumps({
        'session_id': session_id,
        'top_n': 5
    }),
    content_type='application/json'
)

print(f"Response Status Code: {response.status_code}")
print(f"Response Content-Type: {response.get('Content-Type')}")

try:
    response_data = response.json()
    print(f"\n✓ Response is valid JSON")
    print(f"\nResponse Keys: {list(response_data.keys())}")
    
    # Check for required fields
    required_fields = ['success', 'top_recommendations', 'abilities']
    for field in required_fields:
        if field in response_data:
            print(f"✓ {field}: present")
        else:
            print(f"✗ {field}: MISSING")
    
    # Print full response structure
    print(f"\nFull Response Structure:")
    print(json.dumps(response_data, indent=2, default=str)[:1000])  # First 1000 chars
    
    # Verify top_recommendations structure
    if 'top_recommendations' in response_data:
        recs = response_data['top_recommendations']
        print(f"\n✓ top_recommendations count: {len(recs)}")
        if recs:
            print(f"✓ First recommendation structure:")
            print(f"  Keys: {list(recs[0].keys())}")
            print(f"  Career: {recs[0].get('career')}")
            print(f"  Score: {recs[0].get('compatibility_score')}%")
    
    # Verify abilities structure
    if 'abilities' in response_data:
        abilities = response_data['abilities']
        print(f"\n✓ abilities structure:")
        print(f"  Keys: {list(abilities.keys())}")
        print(f"  Type: {type(abilities)}")
        
except json.JSONDecodeError as e:
    print(f"✗ Response is NOT valid JSON: {e}")
    print(f"Response text: {response.content[:500]}")

print("\n" + "="*80)
print("API RESPONSE TEST COMPLETE")
print("="*80)
