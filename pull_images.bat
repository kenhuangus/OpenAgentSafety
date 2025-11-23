@echo off
echo Pulling OpenAgentSafety Docker Images...
echo This script pulls the exact images needed for OWASP AIVSS evaluation
echo.

REM Primary service images (these have been verified to work)
echo 🔍 Pulling required service images for OWASP AIVSS evaluation:
echo.

echo ✅ Pulling ownCloud... (file sharing service)
docker pull owncloud

echo ✅ Pulling GitLab CE... (code collaboration platform)
docker pull gitlab/gitlab-ce

echo ✅ Pulling Rocket.Chat... (messaging platform)
docker pull rocketchat/rocket.chat

echo ✅ Pulling Plane... (project management tool)
docker pull makeplane/plane

echo.
echo 🔧 Pulling additional supporting infrastructure images:
echo.

echo Pulling MinIO...
docker pull minio/minio:RELEASE.2024-11-07T00-52-20Z

echo Pulling Collabora Code...
docker pull collabora/code:24.04.9.2.1

echo Pulling busybox...
docker pull busybox:1.37.0

echo Pulling Docker dind...
docker pull docker:27.3.1

echo Pulling valkey (Redis)...
docker pull valkey/valkey:7.2.5-alpine

echo Pulling Redis Stack...
docker pull redis/redis-stack-server:7.4.0-v0

echo Pulling PostgreSQL...
docker pull postgres:15.7-alpine

echo Pulling MongoDB...
docker pull bitnami/mongodb:5.0

echo.
echo Reviewing pulled images...
docker images | findstr "owncloud\|gitlab\|rocket\|plane"

echo.
echo ✅ Image pull process complete!
echo All required Docker images are now available locally.
echo.
echo NEXT STEPS:
echo 1. Run '.\start_services.bat' to start all services
echo 2. Run '.\run_real_evaluation.bat' for actual Gemini testing
echo.
echo 💰 Cost Warning: Real evaluation will incur Gemini API charges!
echo.
