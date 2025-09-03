@echo off
echo Starting GitHub Repository Analyzer Backend...
echo.

REM Check if .env file exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo ⚠️  Please edit .env file and add your GEMINI_API_KEY
    echo.
)

echo 🚀 Starting FastAPI server...
C:/Python313/python.exe main.py
