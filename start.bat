@echo off
REM Windows startup script for CrowdRisk

echo ========================================
echo   CrowdRisk - Starting Application
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org/
    pause
    exit /b 1
)

echo Starting Backend Server...
start "CrowdRisk Backend" cmd /k "cd backend\app && python main.py"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "CrowdRisk Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   Application Starting...
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to stop all servers...
pause >nul

REM Kill the processes
taskkill /FI "WindowTitle eq CrowdRisk Backend*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq CrowdRisk Frontend*" /T /F >nul 2>&1

echo.
echo Servers stopped.
pause
