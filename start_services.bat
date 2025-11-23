@echo off
echo Starting OpenAgentSafety Docker Services...

REM Navigate to OpenAgentSafety directory where setup.bat is located
cd ..\OpenAgentSafety

REM Check if setup.bat exists
if not exist "setup.bat" (
    echo ❌ setup.bat not found in parent directory
    echo Current directory: %cd%
    dir /b
    pause
    exit /b 1
)

echo ✅ Found setup.bat in: %cd%

echo.
echo Pulling required Docker images...
echo Images will be pulled from approved registries
echo.

REM Pre-pull required images
docker pull ghcr.io/sani903/openagentsafety_base_image-image:1.0.0 2>nul || echo Base image not found at ghcr.io, trying dockerhub...
docker pull sani903/openagentsafety_base_image:latest 2>nul || echo Base image pull failed, will use default

echo.
echo Starting Docker services... This may take 10-15 minutes...
echo Required services:
echo - owncloud:latest (file sharing)
echo - gitlab/gitlab-ce:latest (code collaboration)
echo - rocketchat/rocket.chat:latest (messaging)
echo - makeplane/plane:latest (project management)
echo.

REM Run setup.bat which handles the docker-compose
.\setup.bat

REM Check if services started successfully
echo.
echo Checking if services are running...
docker ps --filter "label=com.docker.compose.project" --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}" 2>nul | findstr "owncloud\|gitlab\|rocketchat\|plane" >nul 2>&1
if errorlevel 1 (
    echo ❌ Services are still starting up. Please wait a few more minutes.
    echo Run 'docker ps' to check status.
) else (
    echo ✅ Services successfully started!
    echo Required services are running.
)

echo.
echo Press any key to return to evaluation...
pause >nul
