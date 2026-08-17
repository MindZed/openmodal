@echo off
if "%1"=="usage" (
    python "%~dp0usage.py"
) else if "%1"=="chat" (
    python "%~dp0chat.py"
) else if "%1"=="setup" (
    python "%~dp0setup.py"
) else (
    echo.
    echo ===================================
    echo       OPENMODAL CLI TOOLKIT
    echo ===================================
    echo.
    echo Usage:
    echo   openmodal setup    - Deploy and configure your AI
    echo   openmodal usage    - View billing and cost monitor
    echo   openmodal chat     - Launch terminal chat with AI
    echo   openmodal help     - Show this help menu
    echo.
)
