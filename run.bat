@echo off
echo ==========================================
echo 🚀 CODEMONK BACKEND - SINGLE COMMAND DEPLOYMENT
echo ==========================================

REM Check Docker
docker version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Docker is not running
    echo Please start Docker Desktop first
    pause
    exit /b 1
)

REM Check Docker Compose
docker compose version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Docker Compose not found
    pause
    exit /b 1
)

echo ✅ Docker is ready

REM Create .env if not exists
if not exist ".env" (
    echo 📝 Creating .env file...
    copy ".env.example" ".env" >nul
    echo ✅ .env file created
)

echo 🛑 Stopping any running containers...
docker compose down >nul 2>&1

echo 🔨 Building containers...
docker compose build --no-cache

echo 🚀 Starting services...
docker compose up -d

echo ⏳ Waiting for services to be ready...
echo    Please wait...

set ready=0
for /l %%i in (1,1,15) do (
    curl -s http://localhost:8000/api/auth/health/ >nul 2>&1
    if not errorlevel 1 (
        set ready=1
        goto :READY
    )
    timeout /t 2 /nobreak >nul
)

:READY
echo.
echo ==========================================
echo 🎉 DEPLOYMENT COMPLETE!
echo ==========================================
echo.
echo 🌐 APPLICATION URLS:
echo    API Server:  http://localhost:8000
echo    Admin Panel: http://localhost:8000/admin
echo    Health:      http://localhost:8000/api/auth/health/
echo.
echo 👤 DEFAULT USERS:
echo    Admin:     admin / Admin@1234
echo    Test User: testuser / Test@1234
echo.
echo 📡 TEST API:
echo    Run test_api.bat
echo.
pause