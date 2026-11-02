@echo off
title Smart-Screenshotter Installer
cd /d "%~dp0"

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ========================================================
    echo  Access denied.
    echo  Please run this script as Administrator.
    echo ========================================================
    pause
    exit /b
)

echo [1/3] Cleaning up previous tasks...
schtasks /end /tn "SmartScreenshotterService" >nul 2>&1
schtasks /delete /tn "SmartScreenshotterService" /f >nul 2>&1
powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*main.py*' } | Stop-Process -Force" >nul 2>&1
timeout /t 1 /nobreak >nul

echo [2/3] Configuring save path...
set /p SAVE_PATH="Enter save path (e.g. D:\Pictures\Screenshots): "

if not exist "%SAVE_PATH%" mkdir "%SAVE_PATH%"
echo {"save_directory": "%SAVE_PATH:\=\\%"} > config.json

echo [3/3] Registering Background Task: SmartScreenshotterService...
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