# Quick Start Guide

## ⚡ 5-Minute Setup

### 1. Backend Setup (Python)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# Train ML model (first time only)
python ml/trainer.py

# Run database migrations
python manage.py migrate

# Populate initial data
python manage.py populate_initial_data

# Start server
python manage.py runserver
```

Server will run at: **http://localhost:8000**

### 2. Frontend Setup (Node.js)

In a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at: **http://localhost:5173**

### 3. Access the Application

1. Open browser to `http://localhost:5173`
2. Click "Start Your Career Assessment"
3. Answer 19 questions across 5 pages
4. Get personalized career recommendations!

---

## 🔑 First Login (Admin Panel)

1. Create superuser (if not already created):
```bash
python manage.py createsuperuser
```

2. Visit: `http://localhost:8000/admin/`
3. Login with created credentials
4. Manage quiz questions, careers, and view results

---

## 📊 Expected Model Accuracy

After training, you should see:
- **Training Accuracy**: 92-96%
- **Test Accuracy**: 85-92%
- **Feature Importance**: Top 5 features identified

---

## ⚠️ Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| Module not found | `pip install -r requirements.txt` |
| Port 8000 in use | `python manage.py runserver 8001` |
| No quiz questions | Run `python manage.py populate_initial_data` |
| Model not found | Run `python ml/trainer.py` |
| CORS errors | Check `CORS_ALLOWED_ORIGINS` in settings.py |
| npm packages fail | Delete `node_modules` and run `npm install` again |

---

## 📱 Features to Test

- [ ] Take quiz from home page
- [ ] Navigate through all 5 quiz pages
- [ ] Submit quiz and get recommendations
- [ ] View compatibility scores
- [ ] See radar chart for abilities
- [ ] Bookmark favorite careers
- [ ] Explore careers page
- [ ] Search for specific careers
- [ ] View course recommendations
- [ ] Mobile responsive on phone/tablet

---

## 🎯 Next Steps After Setup

1. **Customize Careers**: Edit in Django admin
2. **Add More Courses**: Populate database with real courses
3. **Improve ML Model**: Add more training data
4. **Deploy**: See README.md for production deployment
5. **Monetize**: Add payment gateway if needed

---

**Everything working? Great! You're ready for your diploma presentation!** 
