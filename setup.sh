#!/bin/bash
# Career Recommendation System - Automated Setup Script for Mac/Linux

echo ""
echo "=================================================="
echo "Career Recommendation System - Setup Script"
echo "=================================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

echo "[1/8] Versions OK"
python3 --version
node --version
echo ""

# Backend Setup
echo "[2/8] Setting up Backend..."
cd backend

echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[3/8] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[4/8] Training ML Model..."
python ml/trainer.py

echo "[5/8] Setting up database..."
python manage.py migrate

echo "[6/8] Populating initial data..."
python manage.py populate_initial_data

# Return to root
cd ..

# Frontend Setup
echo "[7/8] Setting up Frontend..."
cd frontend
npm install
cd ..

echo "[8/8] Setup Complete!"
echo ""
echo "=================================================="
echo "Setup Completed Successfully!"
echo "=================================================="
echo ""
echo "To start the development servers:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open: http://localhost:5173"
echo ""
