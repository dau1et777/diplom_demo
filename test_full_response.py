#!/usr/bin/env python
"""Quick test to show full API response."""
import requests
import json

API_URL = "http://localhost:8000/api"

# Get questions
resp = requests.get(f"{API_URL}/quiz/questions/")
questions = resp.json().get('results', [])

# Submit quiz
session_id = "test_full_" + str(int(__import__('time').time() * 1000))
answers = {str(q['id']): 8 for q in questions}

requests.post(
    f"{API_URL}/quiz/submit/",
    json={"session_id": session_id, "answers": answers}
)

# Get recommendations
resp = requests.post(
    f"{API_URL}/results/recommend/",
    json={"session_id": session_id, "top_n": 10}
)

data = resp.json()
print("=" * 70)
print("FULL API RESPONSE - Abilities Only")
print("=" * 70)
print(json.dumps(data.get('abilities'), indent=2))

print("\n" + "=" * 70)
print("TOP RECOMMENDATION - Full Detail")
print("=" * 70)
top = data.get('top_recommendations', [{}])[0]
print(json.dumps(top, indent=2)[:500])
print("...")

print(f"\n✓ Total recommendations received: {len(data.get('top_recommendations', []))}")
