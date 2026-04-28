@echo off
REM Helper.ai API Key Setup

echo 🚀 Helper.ai API Key Setup
echo =============================

echo.
echo IMPORTANT: You need an ANTHROPIC API key, not OpenAI!
echo.
echo Steps:
echo 1. Go to: https://console.anthropic.com
echo 2. Sign up for a free account
echo 3. Create an API key (starts with sk-ant-)
echo 4. Copy the key below
echo.

set /p API_KEY="Enter your Anthropic API key (sk-ant-...): "

REM Update the .env file
echo Updating .env file...
powershell -Command "(Get-Content .env) -replace 'ANTHROPIC_API_KEY=.*', 'ANTHROPIC_API_KEY=%API_KEY%' | Set-Content .env"

echo.
echo ✅ API key updated in .env file!
echo.
echo Testing API connection...

python -c "
from ai_engine import generate_ppt
try:
    result = generate_ppt('Test topic')
    print('✅ API connection successful!')
except Exception as e:
    if 'invalid x-api-key' in str(e):
        print('❌ Invalid API key. Please check your Anthropic API key.')
    else:
        print('❌ API test failed:', str(e)[:100])
"

echo.
echo If the test failed, make sure:
echo - You have a valid Anthropic API key (not OpenAI)
echo - Your account has credits
echo - You copied the key correctly
echo.
pause