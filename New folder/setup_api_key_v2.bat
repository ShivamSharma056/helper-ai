@echo off
REM Helper.ai API Key Setup

echo 🚀 Helper.ai API Key Setup
echo =============================

echo.
echo IMPORTANT: You need a REAL Anthropic API key!
echo.
echo Current status: You have placeholder text in your .env file
echo.
echo Steps to get a real API key:
echo =============================
echo 1. Open your web browser
echo 2. Go to: https://console.anthropic.com
echo 3. Sign up for a free account (if you don't have one)
echo 4. Go to API Keys section
echo 5. Create a new API key
echo 6. Copy the key (it will look like: sk-ant-api03-...)
echo.

set /p API_KEY="Paste your REAL Anthropic API key here: "

REM Validate the key format
echo %API_KEY% | findstr /r "sk-ant-" >nul
if %errorlevel% neq 0 (
    echo ❌ Invalid key format! Anthropic keys start with 'sk-ant-'
    echo Please get a proper key from https://console.anthropic.com
    pause
    exit /b 1
)

echo ✅ Key format looks correct!

REM Update the .env file
echo Updating .env file...
powershell -Command "(Get-Content .env) -replace 'ANTHROPIC_API_KEY=.*', 'ANTHROPIC_API_KEY=%API_KEY%' | Set-Content .env"

echo.
echo ✅ API key updated in .env file!
echo.
echo 🔄 Restarting Flask app to load new key...

REM Kill existing Flask processes
powershell -Command "Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*app.py*' } | Stop-Process -Force"

REM Start Flask app
start cmd /k "cd /d %~dp0 && python app.py"

echo.
echo 🧪 Testing API connection...

timeout /t 3 /nobreak >nul

python -c "
from ai_engine import generate_ppt
try:
    result = generate_ppt('Test presentation about artificial intelligence')
    print('✅ API connection successful!')
    print('🎉 Your generate buttons should now work!')
except Exception as e:
    error_str = str(e)
    if 'invalid x-api-key' in error_str:
        print('❌ API key is invalid or expired')
        print('   - Check if your Anthropic account has credits')
        print('   - Try creating a new API key')
    elif 'rate limit' in error_str:
        print('❌ Rate limit exceeded - try again later')
    else:
        print('❌ API test failed:', error_str[:100])
"

echo.
echo 📋 Next steps:
echo - Open http://127.0.0.1:5000 in your browser
echo - Register/Login to your account
echo - Try clicking the generate buttons!
echo.
pause