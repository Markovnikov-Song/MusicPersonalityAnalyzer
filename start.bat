@echo off
chcp 65001 >nul
echo Starting Music Personality Analyzer...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found, please install Python 3.7+
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Start application
echo.
echo Starting web server...
echo Please visit in browser: http://localhost:5000
echo.
python app.py

pause