@echo off
echo 🤖 Starting RBAC Chatbot...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv" (
    echo ⚠️  Virtual environment not found. Creating one...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

echo 🚀 Starting servers...
python start_servers.py

pause 