@echo off
echo Running horoscope generator with DALL-E images, translations, and OpenAI assistant content generation...

:: Set environment variables
set USE_DALLE_IMAGES=true
set USE_TRANSLATIONS=true

:: Check for required environment variables
if "%OPENAI_API_KEY%"=="" (
    echo WARNING: OPENAI_API_KEY is not set. API features may not work correctly.
)

:: Check for astrology assistant IDs
set ASSISTANT_COUNT=0
if not "%EUROPEAN_ASTROLOGY_ASSISTANT_ID%"=="" set /a ASSISTANT_COUNT+=1
if not "%WESTERN_ASTROLOGY_ASSISTANT_ID%"=="" set /a ASSISTANT_COUNT+=1
if not "%CHINESE_ASTROLOGY_ASSISTANT_ID%"=="" set /a ASSISTANT_COUNT+=1
if not "%INDIAN_ASTROLOGY_ASSISTANT_ID%"=="" set /a ASSISTANT_COUNT+=1
if not "%LAL_KITAB_ASSISTANT_ID%"=="" set /a ASSISTANT_COUNT+=1
if not "%KARMIC_ASTROLOGY_ASSISTANT_ID%"=="" set /a ASSISTANT_COUNT+=1
if not "%JYOTISH_ASSISTANT_ID%"=="" set /a ASSISTANT_COUNT+=1
if not "%ESOTERIC_ASTROLOGY_ASSISTANT_ID%"=="" set /a ASSISTANT_COUNT+=1
if not "%NUMEROLOGY_ASSISTANT_ID%"=="" set /a ASSISTANT_COUNT+=1
if not "%TAROT_ASSISTANT_ID%"=="" set /a ASSISTANT_COUNT+=1
if not "%PLANETARY_ASTROLOGY_ASSISTANT_ID%"=="" set /a ASSISTANT_COUNT+=1
if not "%PREDICTIVE_ASTROLOGY_ASSISTANT_ID%"=="" set /a ASSISTANT_COUNT+=1
if not "%LIGHT_ASTROLOGY_ASSISTANT_ID%"=="" set /a ASSISTANT_COUNT+=1
if not "%FORECASTING_ASSISTANT_ID%"=="" set /a ASSISTANT_COUNT+=1
if not "%ASTROLOGY_FORECASTING_ASSISTANT_ID%"=="" set /a ASSISTANT_COUNT+=1

echo Found %ASSISTANT_COUNT% configured astrology assistants
if %ASSISTANT_COUNT% EQU 0 (
    echo WARNING: No astrology assistant IDs are configured. Will use fallback template content.
)

:: Run the horoscope generator
echo Starting horoscope generation process...
python daily_horoscope_replace.py

echo Done!
pause
