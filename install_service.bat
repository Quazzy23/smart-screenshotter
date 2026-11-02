@echo off
title Smart-Screenshotter Installer
cd /d "%~dp0"

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ========================================================
    echo  Access denied.
    echo  Please run this script as Administrator.
    echo ========================================================
    echo.
    pause
    exit /b
)

echo [1/4] Safely stopping old tasks...
schtasks /end /tn "SmartScreenshotterService" >nul 2>&1
schtasks /delete /tn "SmartScreenshotterService" /f >nul 2>&1
powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*main.py*' } | Stop-Process -Force" >nul 2>&1
timeout /t 1 /nobreak >nul

echo [2/4] Checking Python dependencies...
python -m pip install -r requirements.txt

echo [3/4] Configuring save path...
set /p SAVE_PATH="Enter save path (e.g. E:\Screenshots): "

if not exist "%SAVE_PATH%" mkdir "%SAVE_PATH%"
echo {"save_directory": "%SAVE_PATH:\=\\%"} > config.json

echo [4/4] Registering Background Task: SmartScreenshotterService...
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.executable)"') do set PYTHON_PATH=%%i
set PYTHONW_PATH=%PYTHON_PATH:python.exe=pythonw.exe%
set SCRIPT_PATH=%~dp0main.py

schtasks /create /tn "SmartScreenshotterService" /tr "\"%PYTHONW_PATH%\" \"%SCRIPT_PATH%\"" /sc onlogon /f
schtasks /run /tn "SmartScreenshotterService"

echo.
echo ========================================================
echo SUCCESS! Task registered and running!
echo ========================================================
pause