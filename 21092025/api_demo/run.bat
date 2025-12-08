@echo off
REM Beer Sales Prediction API - Quick Start Script for Windows

echo ======================================
echo 🍺 Beer Sales Prediction API
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed.
    echo Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
if not exist "venv\.installed" (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
    type nul > venv\.installed
    echo ✓ Dependencies installed
) else (
    echo ✓ Dependencies already installed
)

REM Check if models exist
if not exist "..\model" (
    echo.
    echo ⚠️  WARNING: Model directory not found!
    echo Please ensure models are trained and saved to ..\model\
    echo Run the beer_sales_prediction_2.ipynb notebook first.
    echo.
    pause
)

REM Start the API
echo.
echo 🚀 Starting API server...
echo    URL: http://localhost:8000
echo    Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.

python main.py

pause

