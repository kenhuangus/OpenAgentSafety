@echo off
echo Installing OpenHands framework for OpenAgentSafety evaluation...
echo.

call owasp_env\Scripts\activate.bat

echo Installing OpenHands from GitHub...
echo This may take several minutes...

pip install git+https://github.com/All-Hands-AI/OpenHands.git

echo.
echo OpenHands installation completed!
echo Now you can run the evaluation scripts.
echo.

pause
