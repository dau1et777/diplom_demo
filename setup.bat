@echo off
REM Career Recommendation System - Automated Setup Script for Windows
REM This script sets up both backend and frontend in one go

echo.
echo ================================================
echo Career Recommendation System - Setup Script
echo ================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/8] Versions OK
python --version
node --version
echo.

REM Backend Setup
echo [2/8] Setting up Backend...
cd backend

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo [3/8] Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo [4/8] Training MI Model...
python ml\trainer.py
if %errorlevel% neq 0 (
    echo WARNING: Model training may have issues
)

echo [5/8] Setting up database...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Database migration failed
    pause
    exit /b 1
)

echo [6/8] Populating initial data...
python manage.py populate_initial_data
if %errorlevel% neq 0 (
    echo WARNING: Initial data population had issues
)

REM Return to root
cd ..

REM Frontend Setup
echo [7/8] Setting up Frontend...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Node dependencies
    pause
    exit /b 1
)
cd ..

echo [8/8] Setup Complete!
echo.
echo ================================================
echo Setup Completed Successfully!
echo ================================================
echo.
echo To start the development servers:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:5173
echo.
pause
