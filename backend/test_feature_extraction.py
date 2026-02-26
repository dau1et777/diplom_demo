#!/usr/bin/env python
"""Test feature extraction with different quiz answers"""

import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.quiz.models import QuizQuestion
from apps.results.inference import CareerInferenceService

# Get all question IDs
questions = QuizQuestion.objects.all().values('id', 'category', 'order')
qid_map = {str(q['id']): (q['category'], q['order']) for q in questions}

# Test scenario 1: Tech-oriented (high logic, low communication, high tech interest)
print("\n" + "="*70)
print("TEST 1: TECH-ORIENTED PROFILE")
print("="*70)
print("Profile: High logic (9), Low communication (4), High tech interest (9)")

answers_tech = {}
for qid, (cat, order) in qid_map.items():
    if cat == 'logic':
        answers_tech[qid] = 9  # high logic
    elif cat == 'creativity':
        answers_tech[qid] = 5  # medium
    elif cat == 'communication':
        answers_tech[qid] = 4  # low communication
    elif cat == 'academic':
        answers_tech[qid] = 8  # good academics
    elif cat == 'interests':
        if order == 14:  # tech interest
            answers_tech[qid] = 9
        else:
            answers_tech[qid] = 3
    elif cat == 'work_style':
        if order == 18:  # independent
            answers_tech[qid] = 8
        else:
            answers_tech[qid] = 3

service = CareerInferenceService()
recs_tech = service.predict_careers(answers_tech, top_n=5)

print(f"\nTop 3 Recommended Careers:")
for i, r in enumerate(recs_tech[:3], 1):
    print(f"  {i}. {r['career']}: {r['compatibility_score']}%")

# Test scenario 2: Creative/Social (low logic, high communication, high creativity)
print("\n" + "="*70)
print("TEST 2: CREATIVE/SOCIAL PROFILE")
print("="*70)
print("Profile: Low logic (3), High communication (9), High creativity (9)")

answers_creative = {}
for qid, (cat, order) in qid_map.items():
    if cat == 'logic':
        answers_creative[qid] = 3  # low logic
    elif cat == 'creativity':
        answers_creative[qid] = 9  # high creativity
    elif cat == 'communication':
        answers_creative[qid] = 9  # high communication
    elif cat == 'academic':
        answers_creative[qid] = 6  # average academics
    elif cat == 'interests':
        if order == 16:  # creativity interest
            answers_creative[qid] = 9
        elif order == 17:  # social interest
            answers_creative[qid] = 8
        else:
            answers_creative[qid] = 3
    elif cat == 'work_style':
        if order == 19:  # collaborative
            answers_creative[qid] = 8
        else:
            answers_creative[qid] = 3

recs_creative = service.predict_careers(answers_creative, top_n=5)

print(f"\nTop 3 Recommended Careers:")
for i, r in enumerate(recs_creative[:3], 1):
    print(f"  {i}. {r['career']}: {r['compatibility_score']}%")

# Compare
print("\n" + "="*70)
print("COMPARISON: Are recommendations different?")
print("="*70)
tech_careers = [r['career'] for r in recs_tech[:3]]
creative_careers = [r['career'] for r in recs_creative[:3]]
print(f"Tech profile top careers:     {tech_careers}")
print(f"Creative profile top careers: {creative_careers}")
print(f"Are they different? {tech_careers != creative_careers}")
