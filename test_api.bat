@echo off
echo 🧪 CODEMONK BACKEND API TESTING
echo ================================

set BASE_URL=http://localhost:8000
set COOKIE_FILE=test_cookies.txt

echo ⏳ Waiting for API...
timeout /t 10 /nobreak >nul

echo.
echo 🔍 Testing Health Check...
curl -s %BASE_URL%/api/auth/health/
echo.

echo.
echo 📝 Testing Register User...
curl -X POST %BASE_URL%/api/auth/register/ ^
 -H "Content-Type: application/json" ^
 -d "{\"username\":\"apitest\",\"password\":\"Test@1234\"}"
echo.

echo.
echo 🔐 Testing Login...
curl -X POST %BASE_URL%/api/auth/login/ ^
 -H "Content-Type: application/json" ^
 -d "{\"username\":\"apitest\",\"password\":\"Test@1234\"}" ^
 -c %COOKIE_FILE%
echo.

echo.
echo 📄 Testing Submit Paragraphs...
curl -X POST %BASE_URL%/api/text/submit/ ^
 -H "Content-Type: application/json" ^
 -d "{\"paragraphs\":[\"This is test paragraph\",\"Another test paragraph\"]}" ^
 -b %COOKIE_FILE%
echo.

echo ⏳ Waiting for background processing...
timeout /t 5 /nobreak >nul

echo.
echo 🔎 Testing Search Word...
curl -X GET "%BASE_URL%/api/text/search/?word=test" ^
 -b %COOKIE_FILE%
echo.

echo.
echo 🚪 Testing Logout...
curl -X POST %BASE_URL%/api/auth/logout/ ^
 -H "Content-Type: application/json" ^
 -b %COOKIE_FILE%
echo.

del %COOKIE_FILE% 2>nul

echo ========================================
echo 🎉 API TESTING COMPLETE!
echo ========================================
echo ✅ All endpoints executed
echo 🌐 Access: http://localhost:8000
pause