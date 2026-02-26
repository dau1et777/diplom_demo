# System Architecture & Design Document

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
│              React + Vite + Tailwind CSS                       │
│  (QuizPage, ResultsPage, CareersPage, Visualizations)         │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTP/REST API
                          │ (JSON)
┌─────────────────────────▼───────────────────────────────────────┐
│                     API LAYER                                   │
│           Django REST Framework (DRF)                           │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  Quiz API        │  │  Careers API     │  │  Results API │ │
│  │  (endpoints)     │  │  (endpoints)     │  │  (inference) │ │
│  └────────┬─────────┘  └────────┬─────────┘  └──────┬───────┘ │
└───────────┼────────────────────┼──────────────────┼───────────┘
            │                    │                  │
┌───────────▼────────────────────▼──────────────────▼───────────┐
│                   BUSINESS LOGIC LAYER                         │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  │
│  │  Quiz Manager  │  │  Career Manager │  │ Inference     │  │
│  │  - Validate    │  │  - Query data  │  │ Service       │  │
│  │  - Process    │  │  - Format info │  │  - Load model │  │
│  └────────────────┘  └────────────────┘  │  - Predict   │  │
│                                          │  - Score     │  │
│                                          └────────────────┘  │
│                                                               │
│                   ML INFERENCE LAYER                          │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ CareerPredictor                                           ││
│  │ - Feature extraction from quiz answers                   ││
│  │ - Normalization (StandardScaler)                         ││
│  │ - RandomForestClassifier prediction                      ││
│  │ - Top-5 recommendations with probabilities              ││
│  └──────────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼──────────────────────────────────────┐
│                   DATA LAYER                                   │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  DATABASE (PostgreSQL / SQLite)                          │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│ │
│  │  │  Quiz    │  │ Careers  │  │ Results  │  │   User   ││ │
│  │  │  Tables  │  │  Tables  │  │  Tables  │  │ Progress ││ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘│ │
│  └──────────────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  ML MODELS (File System)                                 │ │
│  │  ├─ career_model.joblib (RandomForest)                  │ │
│  │  ├─ scaler.joblib (StandardScaler)                      │ │
│  │  └─ label_encoder.joblib (Career labels)                │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

---

## Component Diagram

```
FRONTEND COMPONENTS
├── Header (Navigation, Branding)
├── HomePage (Landing, Features, CTAs)
├── QuizPage
│   ├── Question Display
│   ├── Range Slider (1-10)
│   ├── Progress Bar
│   ├── Pagination (5 per page)
│   └── Submit Button
├── ResultsPage
│   ├── Primary Recommendation Card
│   ├── Stats Summary
│   ├── BarChart (Top 5 Careers)
│   ├── RadarChart (Abilities)
│   ├── Career List (Scrollable)
│   ├── Bookmark Feature
│   └── Action Buttons
└── CareersPage
    ├── Search Input
    ├── Career List (Scrollable)
    ├── Career Details Panel
    ├── Skills Display
    ├── Courses List
    └── Universities List

BACKEND COMPONENTS
├── Django Settings (config/)
├── Quiz App (apps/quiz/)
│   ├── Models
│   │   ├── QuizQuestion
│   │   ├── QuizAnswer
│   │   └── QuizSubmission
│   ├── Serializers
│   ├── Views (REST)
│   └── Admin Interface
├── Careers App (apps/careers/)
│   ├── Models
│   │   ├── Career
│   │   ├── Course
│   │   └── University
│   ├── Serializers
│   ├── Views (REST)
│   └── Management Commands
├── Results App (apps/results/)
│   ├── Models
│   │   ├── CareerRecommendation
│   │   └── UserProgress
│   ├── Serializers
│   ├── Views (REST)
│   └── Inference Service
└── ML Module (ml/)
    ├── trainer.py (Training pipeline)
    ├── predictor.py (Model loading/prediction)
    ├── data/ (Datasets)
    └── models/ (Serialized models)
```

---

## Data Flow Diagram

### User Quiz Submission Flow
```
User Takes Quiz
    ↓
[Frontend] Collects answers (19 questions, 1-10 scale)
    ↓
Saves to Session Storage (backup)
    ↓
Sends POST to /api/quiz/submit/
    {
        "session_id": "unique_id",
        "answers": {
            "question_uuid": response_int,
            ...
        }
    }
    ↓
[Backend] QuizSubmissionViewSet.submit_quiz()
    ↓
[Database] Saves QuizSubmission & QuizAnswer records
    ↓
Returns success response
    ↓
[Frontend] Triggers recommendation generation
```

### Recommendation Generation Flow
```
User Clicks "Submit & Get Results"
    ↓
[Frontend] POST /api/results/recommend/
    {
        "session_id": "session_id",
        "top_n": 5
    }
    ↓
[Backend] CareerRecommendationViewSet.generate_recommendations()
    ↓
Fetches QuizAnswer records for session
    ↓
[Inference] CareerInferenceService.predict_careers()
    ├─ extract_features_from_quiz() → 16 features
    ├─ get_numeric_features_array() → normalized array
    ├─ predictor.predict_top_careers() → probabilities
    └─ Add explanations & skills
    ↓
Returns top 5 careers with compatibility % (0-100)
    ↓
[Database] Saves CareerRecommendation record
    ↓
[Frontend] Displays results page with charts
```

### Career Browse Flow
```
User Clicks "Explore All Careers"
    ↓
[Frontend] GET /api/careers/
    ↓
[Backend] CareerViewSet.list()
    ↓
Returns all active careers with basic info
    ↓
[Frontend] Displays career list
    ↓
User Selects Career
    ↓
[Frontend] GET /api/careers/{career_id}/
    ↓
[Backend] Loads full details:
    - Description
    - Required skills
    - Salary range
    - Related courses (via FK)
    - Related universities (via FK)
    ↓
[Frontend] Displays comprehensive career details
```

---

## Database Schema

### Quiz Tables
```
QuizQuestion
├── id (UUID, PK)
├── question_text (CharField)
├── category (ChoiceField: logic, creativity, communication, academic, interests, work_style)
├── description (TextField)
├── order (IntegerField)
├── is_active (BooleanField)
├── created_at (DateTimeField)
└── updated_at (DateTimeField)

QuizAnswer
├── id (UUID, PK)
├── question (FK → QuizQuestion)
├── user_response (IntegerField, 1-10)
├── session_id (CharField, indexed)
└── submitted_at (DateTimeField, indexed)

QuizSubmission
├── id (UUID, PK)
├── session_id (CharField, unique, indexed)
├── user (FK → User, nullable)
├── submitted_at (DateTimeField, indexed)
```

### Career Tables
```
Career
├── id (UUID, PK)
├── name (CharField, unique, indexed)
├── description (TextField)
├── required_skills (JSONField, array)
├── suitable_for (TextField)
├── average_salary_range (CharField)
├── job_growth (CharField)
├── typical_companies (JSONField, array)
├── required_education (CharField)
├── related_careers (JSONField, array)
├── is_active (BooleanField)
├── created_at (DateTimeField)
└── updated_at (DateTimeField)

Course
├── id (UUID, PK)
├── career (FK → Career)
├── name (CharField)
├── provider (CharField)
├── url (URLField)
├── description (TextField)
├── duration (CharField)
├── difficulty_level (ChoiceField: beginner, intermediate, advanced)
├── is_active (BooleanField)
└── created_at (DateTimeField)

University
├── id (UUID, PK)
├── career (FK → Career)
├── name (CharField)
├── location (CharField)
├── program_name (CharField)
├── url (URLField)
├── ranking (IntegerField, nullable)
├── is_active (BooleanField)
└── created_at (DateTimeField)
```

### Results Tables
```
CareerRecommendation
├── id (UUID, PK)
├── session_id (CharField, unique, indexed)
├── user (FK → User, nullable)
├── primary_career (CharField)
├── primary_compatibility (FloatField, 0-100)
├── top_recommendations (JSONField)
│   [
│     {
│       "career": "Software Developer",
│       "compatibility_score": 87.5,
│       "probability": 0.875,
│       "explanation": "...",
│       "required_skills": [...],
│       "suitable_for": "..."
│     },
│     ...
│   ]
├── abilities (JSONField)
│   {
│     "logical_thinking": 8.2,
│     "creativity": 6.5,
│     ...
│   }
├── quiz_features (JSONField)
├── created_at (DateTimeField, indexed)
└── updated_at (DateTimeField)

UserProgress
├── id (UUID, PK)
├── session_id (CharField, indexed)
├── user (FK → User, nullable)
├── recommendation (FK → CareerRecommendation)
├── quiz_attempt (IntegerField)
├── viewed_careers (JSONField, array of career IDs)
├── saved_careers (JSONField, array of career IDs)
├── take_quiz_count (IntegerField)
├── created_at (DateTimeField, indexed)
└── updated_at (DateTimeField)
```

---

## ML Model Architecture

### Feature Engineering
```
Quiz Answers (19 questions, 1-10 scale)
    ↓
[Feature Extraction Service]
    ├─ Group by question category
    ├─ Convert to numeric scale (1-10 or 0-1)
    └─ Normalize values
    ↓
Feature Vector (16 features)
┌─────────────────────────────────────────────────────────────┐
│                     FEATURE VECTOR                          │
├─────────────────────────────────────────────────────────────┤
│ Continuous Features (normalized to 0-1):                    │
│  1. logical_thinking (0-1, from Q1-3 avg)                  │
│  2. creativity (0-1, from Q4-6 avg)                        │
│  3. communication (0-1, from Q7-9 avg)                     │
│  4. problem_solving (derived)                              │
│  5. teamwork (derived)                                      │
│  6. leadership (derived)                                    │
│  7. math_score (0-100)                                     │
│  8. english_score (0-100)                                  │
│  9. science_score (0-100)                                  │
│ 10. art_score (0-100)                                      │
│                                                             │
│ Binary Features:                                            │
│ 11. interest_tech (0 or 1)                                 │
│ 12. interest_business (0 or 1)                             │
│ 13. interest_creativity (0 or 1)                           │
│ 14. interest_social (0 or 1)                               │
│ 15. work_style_independent (0 or 1)                        │
│ 16. work_style_collaborative (0 or 1)                      │
└─────────────────────────────────────────────────────────────┘
    ↓
[Normalization]
StandardScaler: mean=0, std=1
    ↓
[Random Forest Classifier]
    ├─ 200 decision trees
    ├─ Max depth: 15
    ├─ Class weights: balanced
    └─ Training: ~80 samples
    ↓
[Output: Probability Per Class]
Software Developer:     0.865 (86.5%)
Data Scientist:         0.782 (78.2%)
AI/ML Engineer:         0.651 (65.1%)
...
    ↓
[Post-Processing]
├─ Sort by probability
├─ Top 5 recommendations
├─ Add explanations
└─ Format for frontend
```

### Training Pipeline
```python
CareerModelTrainer.run_full_pipeline()
    ├─ Load dataset (csv)
    ├─ Prepare data (split features/target)
    ├─ Train-test split (80/20)
    ├─ Normalize features (StandardScaler)
    ├─ Train model (RandomForest)
    ├─ Evaluate (accuracy, precision, recall)
    ├─ Feature importance analysis
    └─ Save artifacts (model, scaler, encoder)
        ├─ career_model.joblib
        ├─ scaler.joblib
        └─ label_encoder.joblib
```

---

## API Request/Response Examples

### 1. Get Quiz Questions
```
GET /api/quiz/questions/

Response 200 OK:
{
  "count": 19,
  "results": [
    {
      "id": "uuid-1",
      "question_text": "How would you rate your logical thinking?",
      "category": "logic",
      "category_display": "Logical Thinking",
      "description": "Question assessment description",
      "order": 1
    },
    ...
  ]
}
```

### 2. Submit Quiz
```
POST /api/quiz/submit/
Content-Type: application/json

{
  "session_id": "session_12345_abc",
  "answers": {
    "question-uuid-1": 8,
    "question-uuid-2": 7,
    "question-uuid-3": 9,
    ...
    "question-uuid-19": 6
  }
}

Response 201 Created:
{
  "success": true,
  "submission_id": "uuid",
  "session_id": "session_12345_abc",
  "message": "Quiz submitted successfully"
}
```

### 3. Generate Recommendations
```
POST /api/results/recommend/
Content-Type: application/json

{
  "session_id": "session_12345_abc",
  "top_n": 5
}

Response 201 Created:
{
  "success": true,
  "recommendation_id": "uuid",
  "session_id": "session_12345_abc",
  "primary_career": "Software Developer",
  "primary_compatibility": 87.5,
  "top_recommendations": [
    {
      "career": "Software Developer",
      "compatibility_score": 87.5,
      "probability": 0.875,
      "explanation": "Strong logical thinking and tech interest...",
      "required_skills": ["Python", "JavaScript", "Design Patterns"],
      "suitable_for": "High logical thinking, tech interest, good math"
    },
    {
      "career": "Data Scientist",
      "compatibility_score": 78.2,
      "probability": 0.782,
      ...
    },
    ...
  ],
  "abilities": {
    "logical_thinking": 8,
    "creativity": 6,
    "communication": 7,
    "problem_solving": 8,
    "leadership": 5,
    "academic_performance": 7.8
  }
}
```

### 4. Get All Careers
```
GET /api/careers/

Response 200 OK:
{
  "count": 18,
  "results": [
    {
      "id": "uuid",
      "name": "Software Developer",
      "description": "Develops applications...",
      "average_salary_range": "$80k - $150k",
      "job_growth": "15% annual"
    },
    ...
  ]
}
```

### 5. Get Career Details
```
GET /api/careers/{id}/

Response 200 OK:
{
  "id": "uuid",
  "name": "Software Developer",
  "description": "Develops applications using programming languages...",
  "required_skills": ["Python", "JavaScript", "System Design"],
  "suitable_for": "High logical thinking, tech interest...",
  "average_salary_range": "$80k - $150k",
  "job_growth": "15% annual",
  "typical_companies": ["Google", "Microsoft", "Apple"],
  "required_education": "Bachelor in Computer Science",
  "related_careers": ["Backend Developer", "Data Scientist"],
  "courses": [
    {
      "id": "uuid",
      "name": "Python for Beginners",
      "provider": "Udemy",
      "url": "https://...",
      "description": "...",
      "duration": "4 weeks",
      "difficulty_level": "beginner"
    }
  ],
  "universities": [
    {
      "id": "uuid",
      "name": "MIT",
      "location": "Cambridge, MA",
      "program_name": "Bachelor of Computer Science",
      "url": "https://...",
      "ranking": 1
    }
  ]
}
```

---

## Frontend State Management

### Session Storage (Quiz Progress)
```javascript
sessionStorage = {
  sessionId: "session_12345_abc",
  quizAnswers: {
    "question-1": 8,
    "question-2": 7,
    ...
  },
  results: {
    // Full results from server
  }
}
```

### Local Storage (Bookmarks)
```javascript
localStorage = {
  bookmarks: [
    "Software Developer",
    "Data Scientist",
    ...
  ]
}
```

---

## Security Considerations

1. **CORS**: Restricted to allowed origins
2. **Environment Variables**: Sensitive data in .env
3. **Validation**: All inputs validated server-side
4. **Serialization**: DRF serializers for data validation
5. **No Authentication Required**: System allows anonymous usage
6. **Rate Limiting**: Can be added via middleware
7. **HTTPS**: Required in production
8. **CSRF Protection**: Enabled in Django

---

## Performance Optimization

### Frontend
- React lazy loading for components
- Recharts optimized for ~5 data points
- Session storage for offline capability
- Responsive images
- CSS minification via Vite

### Backend
- Database indexing on frequently queried fields (session_id, created_at)
- DRF pagination for large datasets
- QuerySet optimization (.select_related, .prefetch_related)
- ML model caching in memory
- StandardScaler precomputed at training

### ML Model
- Model complexity: 200 trees (fast prediction)
- Feature count: 16 (minimal memory footprint)
- Inference time: <100ms per request
- Joblib serialization: efficient storage

---

## Scalability Considerations

### Database Scaling
- Use PostgreSQL for production (SQLite limited)
- Add database indexes
- Implement connection pooling
- Archive old results periodically

### API Scaling
- Use load balancer (Nginx, HAProxy)
- Deploy multiple Django instances
- Use Celery for async tasks
- Implement caching (Redis)

### Frontend Scaling
- Use CDN for static files
- Implement code splitting
- Minify all assets
- Use service workers for offline support

---

## Testing Strategy

### Unit Tests (to implement)
- Model tests
- Serializer tests
- API endpoint tests
- ML inference tests

### Integration Tests
- End-to-end API flows
- Database transactions
- ML pipeline end-to-end

### Frontend Tests
- Component rendering
- API mocking
- User interactions
- Browser compatibility

---

## Deployment Checklist

- [ ] Update SECRET_KEY in .env
- [ ] Set DEBUG=False
- [ ] Configure allowed hosts
- [ ] Set up PostgreSQL database
- [ ] Run migrations
- [ ] Collect static files
- [ ] Set up SSL/HTTPS
- [ ] Configure email backend
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Load test the system
- [ ] Document deployment process

---

**Document Version**: 1.0
**Last Updated**: February 2025
**Status**: Complete
