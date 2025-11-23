@echo off
echo Setting up OWASP AIVSS virtual environment...

REM Create virtual environment
python -m venv owasp_env
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    exit /b 1
)
echo ✓ Virtual environment created

REM Activate and install dependencies
call owasp_env\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    exit /b 1
)
echo ✓ Virtual environment activated

REM Upgrade pip
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Error: Failed to upgrade pip
    exit /b 1
)
echo ✓ Pip upgraded

REM Install core dependencies
pip install PyYAML tomli
if errorlevel 1 (
    echo Error: Failed to install core dependencies
    exit /b 1
)
echo ✓ Core dependencies installed (PyYAML, tomli)

REM Install additional evaluation dependencies
pip install openai requests
if errorlevel 1 (
    echo Warning: Failed to install some dependencies - may not be critical
)
echo ✓ Additional dependencies installed (where available)

echo.
echo 🎉 Setup complete! Virtual environment is ready.
echo To activate the environment later, run: owasp_env\Scripts\activate.bat
echo.
