@echo off
echo Running horoscope generator with DALL-E image generation...

:: Set environment variables
set USE_DALLE_IMAGES=true

:: Run the horoscope generator
python daily_horoscope_replace.py

echo Done!
pause
