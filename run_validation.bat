@echo off
echo Running OWASP AIVSS Tasks Validation...

REM Activate virtual environment
call owasp_env\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Error: Failed to activate virtual environment
    exit /b 1
)

REM Change to evaluation directory and run validation
cd evaluation
python validate_owasp_tasks.py

REM Check if validation was successful
if errorlevel 1 (
    echo ❌ Validation failed or no tasks found properly implemented
) else (
    echo ✅ Validation completed successfully
)

echo.
echo Press any key to continue...
pause >nul
