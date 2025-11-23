@echo off
echo Running Risk #1: Tool Misuse Evaluation with real Gemini-2.5-pro API calls
echo.

cd evaluation
call ..\owasp_env\Scripts\activate.bat

echo Starting Tool Misuse vulnerability assessment...
echo This will make real API calls to Gemini-2.5-pro
echo.
echo ⚠️  WARNING: This costs real API credits!
echo.
echo Command: python run_eval.py --agent-llm-config test_agent --env-llm-config test_env --task-path ../workspaces/tasks/safety-tool-squatting --server-hostname localhost
echo.

pause Press any key to start actual red teaming evaluation...

python run_eval.py --agent-llm-config test_agent --env-llm-config test_env --task-path ../workspaces/tasks/safety-tool-squatting --server-hostname localhost

echo.
echo Evaluation completed!
echo Check above output for Gemini's actual safety behaviors and scores.
echo.
pause
