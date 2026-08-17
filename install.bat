@echo off
setlocal
echo ===================================================
echo 🔥 Mindzed Technologies Setup Launcher 🔥
echo ===================================================

:: Check if Python is already installed
python --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo =^> Python detected.
    goto run_setup
)

echo [!] Python is not installed.
set /p install_choice="? Do you want to automatically install Python using winget? (y/n): "
IF /I "%install_choice%"=="y" (
    echo =^> Installing Python...
    winget install --id Python.Python.3.12 --exact --silent --accept-package-agreements --accept-source-agreements
    
    :: Refresh PATH for the current session to ensure Python is detected
    call RefreshEnv.cmd 2>nul
    
    python --version >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo [-] Python installation finished, but it is not available in your PATH yet.
        echo [-] Please restart your terminal and run this script again.
        pause
        exit /b 1
    )
) ELSE (
    echo Exiting. Please install Python to continue.
    pause
    exit /b 1
)

:run_setup
echo =^> Adding OpenModal to User PATH for global access...
powershell -NoProfile -Command "$curr = [Environment]::GetEnvironmentVariable('Path', 'User'); $dir = (Get-Location).Path; if ($curr -notlike ('*' + $dir + '*')) { [Environment]::SetEnvironmentVariable('Path', $curr + ';' + $dir, 'User'); Write-Host '=> OpenModal added to PATH.' }"

echo =^> Launching Interactive Setup...
python setup.py
pause
