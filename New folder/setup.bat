@echo off
REM Helper.ai Setup Script

echo 🚀 Helper.ai Setup
echo ===================

REM Check if Anthropic API key is set
echo Checking Anthropic API key...
if "%ANTHROPIC_API_KEY%"=="" (
    echo ❌ ANTHROPIC_API_KEY not set!
    echo.
    echo To fix this:
    echo 1. Go to https://console.anthropic.com
    echo 2. Get your API key
    echo 3. Run: set ANTHROPIC_API_KEY=your-api-key-here
    echo 4. Or create a .env file with: ANTHROPIC_API_KEY=your-api-key-here
    echo.
    pause
    exit /b 1
) else (
    echo ✅ ANTHROPIC_API_KEY is set
)

REM Test the API
echo.
echo Testing API connection...
python -c "
import os
from ai_engine import generate_ppt
try:
    # Test with a simple topic
    result = generate_ppt('Test Topic')
    print('✅ API connection successful!')
    print('Response preview:', str(result)[:100] + '...')
except Exception as e:
    print('❌ API test failed:', str(e))
"

echo.
echo Setup complete! You can now use the generate features.
echo Make sure you're logged in to the web app.
pause