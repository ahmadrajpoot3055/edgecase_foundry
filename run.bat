@echo off
setlocal enabledelayedexpansion
title EdgeCase Foundry

echo ========================================================
echo   EdgeCase Foundry - Minimalist Edge-Case Testing
echo ========================================================
echo.

if exist .env (
    for /f "usebackq tokens=1* delims==" %%a in (".env") do (
        set "key=%%a"
        if not "!key:~0,1!"=="#" (
            set "%%a=%%b"
        )
    )
    echo [*] Environment loaded from .env
)

if not exist ".venv\Scripts\streamlit.exe" (
    echo [!] Virtual environment not found in .venv.
    echo [*] Setting up virtual environment...
    python -m venv .venv
    .\.venv\Scripts\pip install -r requirements.txt
)

echo [*] Starting Streamlit server...
echo [*] Open your browser to the local URL shown below.
echo.
.\.venv\Scripts\streamlit.exe run app.py
if errorlevel 1 (
    echo.
    echo Streamlit exited with error code %errorlevel%.
    pause
)
