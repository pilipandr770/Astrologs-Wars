@echo off
echo Running horoscope generator with DALL-E images and translations...

:: Set environment variables
set USE_DALLE_IMAGES=true
set USE_TRANSLATIONS=true

:: Run the horoscope generator
python daily_horoscope_replace.py

echo Done!
pause
