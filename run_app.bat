@echo off
setlocal EnableDelayedExpansion
title Roland Garros Finals Explorer

echo.
echo ========================================
echo 🎾 Roland Garros Finals Explorer
echo ========================================
echo.

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call .venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else (
    echo ⚠️ Virtual environment not found, using system Python
)

echo.
echo 📦 Checking dependencies...

REM Check if requirements.txt exists
if exist "requirements.txt" (
    echo 📋 Installing/updating dependencies...
    pip install -r requirements.txt --quiet
    if !errorlevel! equ 0 (
        echo ✅ Dependencies installed successfully
    ) else (
        echo ❌ Error installing dependencies
        pause
        exit /b 1
    )
) else (
    echo ⚠️ requirements.txt not found, installing basic dependencies...
    pip install streamlit pandas numpy matplotlib seaborn plotly --quiet
)

echo.
echo 🔍 Checking data file...
if exist "roland_garros_finals_2000_2025.csv" (
    echo ✅ Data file found
) else (
    echo ❌ Data file not found!
    echo Please ensure 'roland_garros_finals_2000_2025.csv' is in the current directory
    pause
    exit /b 1
)

echo.
echo 🔍 Checking app file...
if exist "app.py" (
    echo ✅ App file found
) else (
    echo ❌ App file not found!
    echo Please ensure 'app.py' is in the current directory
    pause
    exit /b 1
)

echo.
echo 🚀 Launching Roland Garros Finals Explorer...
echo.
echo 📱 The app will open in your default browser
echo 🔗 URL: http://localhost:8501
echo.
echo ⏹️ Press Ctrl+C to stop the app
echo.

REM Start Streamlit with some optimizations
streamlit run app.py --server.headless false --server.enableCORS false --server.enableXsrfProtection false

echo.
echo 🛑 App stopped
pause 