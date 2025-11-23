@echo off
echo Setting up Plane project management tool...
echo.

REM Create separate directory for Plane
if not exist "plane_setup" (
    mkdir plane_setup
)
cd plane_setup

echo 1. Cloning Plane repository...
git clone https://github.com/jamsocket/plane.git
if errorlevel 1 (
    echo ❌ Failed to clone Plane repository
    cd ..
    exit /b 1
)

cd plane

echo 2. Starting Plane services with docker-compose...
echo This will start:
echo - Postgres database
echo - Plane controller
echo - Plane drone
echo - Plane proxy
echo.
echo Press Ctrl+C to stop Plane services when ready...
echo.

docker compose -f docker/docker-compose.yml up

echo.
echo Plane services stopped.
echo Note: Plane should be running in a separate terminal/command window
echo for the OpenAgentSafety evaluation to work.
echo.
