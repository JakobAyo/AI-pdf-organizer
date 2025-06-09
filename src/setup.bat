@echo off
:: One-Click Python + Pip + Requirements Installer for Windows
:: Properly handles Python detection and reinstallation
:: Just double-click this file to run it

:: Check if running with admin rights
NET SESSION >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Running with admin privileges
) else (
    echo Requesting admin privileges...
    :: Re-launch with admin rights
    PowerShell -Command "Start-Process cmd -ArgumentList '/c %~dpnx0' -Verb RunAs"
    exit /b
)

:: Set console window title
title Python One-Click Installer

:: Configuration
set PYTHON_VERSION=3.10.11
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe
set INSTALLER_PATH=%TEMP%\python_installer.exe
set INSTALL_DIR=C:\Python%PYTHON_VERSION%

echo ########################################################
echo #        Python One-Click Installation Script          #
echo ########################################################
echo.

:: Store the script's directory
set "SCRIPT_DIR=%~dp0"
echo Script running from: %SCRIPT_DIR%
echo.

:: Improved Python detection
echo Checking Python installation...
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Python appears to be installed:
    python --version 2>nul || (
        echo ERROR: Python is in PATH but not working properly
        echo Forcing reinstallation...
        goto INSTALL_PYTHON
    )
    goto CHECK_REQUIREMENTS
) else (
    echo Python not found in PATH
    :: Additional check for Python installation
    if exist "%INSTALL_DIR%\python.exe" (
        echo Found Python in %INSTALL_DIR% but not in PATH
        echo Adding Python to PATH...
        setx PATH "%INSTALL_DIR%;%INSTALL_DIR%\Scripts;%PATH%"
        goto CHECK_REQUIREMENTS
    )
)

:INSTALL_PYTHON
:: Download Python installer
echo Downloading Python %PYTHON_VERSION%...
powershell -Command "(New-Object Net.WebClient).DownloadFile('%PYTHON_URL%', '%INSTALLER_PATH%')"
if not exist "%INSTALLER_PATH%" (
    echo Failed to download Python installer
    pause
    exit /b 1
)

:: Install Python silently
echo Installing Python %PYTHON_VERSION%...
start /wait "" "%INSTALLER_PATH%" /quiet InstallAllUsers=1 PrependPath=1 TargetDir="%INSTALL_DIR%" Include_launcher=1 Include_test=0
del "%INSTALLER_PATH%"

:: Refresh PATH
echo Refreshing environment variables...
call refreshenv >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    powershell -Command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'Machine'), 'Process')"
)

:: Verify installation
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python installation failed
    pause
    exit /b 1
)

:CHECK_REQUIREMENTS
echo.
echo Verifying Python installation...
python --version || (
    echo ERROR: Python is not working after installation
    echo Please restart your computer and run this installer again
    pause
    exit /b 1
)
echo Python installed successfully
echo.

:: Check if pip is available
python -m pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing pip...
    python -m ensurepip --upgrade || (
        echo Failed to install pip
        pause
        exit /b 1
    )
)

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip || (
    echo Failed to upgrade pip
    pause
    exit /b 1
)

:: Check for requirements.txt in script directory
echo Checking for requirements.txt in: %SCRIPT_DIR%
if exist "%SCRIPT_DIR%requirements.txt" (
    echo Found requirements.txt
    echo Installing requirements...
    cd /d "%SCRIPT_DIR%"
    python -m pip install --upgrade -r requirements.txt || (
        echo Failed to install some requirements
        pause
        exit /b 1
    )
    echo Requirements installed:
    type "%SCRIPT_DIR%requirements.txt"
) else (
    echo No requirements.txt found in script directory
    echo Create requirements.txt in the same folder as this installer
    echo to automatically install Python packages.
)

:: Final check
echo.
echo Final verification:
echo Python version: 
python --version
echo Pip version:
python -m pip --version
echo.
echo Installation complete!
echo You can now close this window.
pause