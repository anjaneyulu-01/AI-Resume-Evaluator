# run.ps1 - PowerShell script to install and run the Resume ATS Checker
# Run this with: powershell -ExecutionPolicy Bypass -File run.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Resume ATS Score Checker Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pip is installed
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✓ pip is ready: $pipVersion" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: pip is not installed" -ForegroundColor Red
    Write-Host "Please reinstall Python with pip included" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing required packages..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Yellow
Write-Host ""

# Install dependencies
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Write-Host "Please ensure you have internet connection and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "✓ All packages installed successfully!" -ForegroundColor Green
Write-Host ""

# Run the Streamlit app
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Resume ATS Checker" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your browser should open automatically at:" -ForegroundColor Cyan
Write-Host "http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
Write-Host "To stop the server, press Ctrl+C" -ForegroundColor Yellow
Write-Host ""

streamlit run app.py

Read-Host "Press Enter to exit"
