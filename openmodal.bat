@echo off
if "%1"=="usage" (
    python usage.py
) else if "%1"=="chat" (
    python chat.py
) else (
    echo.
    echo ===================================
    echo       OPENMODAL CLI TOOLKIT
    echo ===================================
    echo.
    echo Usage:
    echo   openmodal usage    - View billing and cost monitor
    echo   openmodal chat     - Launch terminal chat with AI
    echo.
)
