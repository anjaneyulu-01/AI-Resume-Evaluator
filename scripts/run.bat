@echo off
REM Resume ATS Checker - Setup and Run Script
REM This script will install dependencies and run the application

echo.
echo ========================================
echo   Resume ATS Score Checker Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✓ Python found: 
python --version
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is not installed
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo ✓ pip is ready
echo.

REM Install dependencies
echo Installing required packages...
echo This may take a few minutes...
echo.

pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please ensure you have internet connection and try again
    pause
    exit /b 1
)

echo.
echo ✓ All packages installed successfully!
echo.

REM Run the Streamlit app
echo ========================================
echo   Starting Resume ATS Checker
echo ========================================
echo.
echo Your browser should open automatically at:
echo http://localhost:8501
echo.
echo To stop the server, press Ctrl+C
echo.

streamlit run app.py

pause
