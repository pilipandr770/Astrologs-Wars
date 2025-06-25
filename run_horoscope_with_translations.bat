@echo off
echo Running horoscope generator with translations...

:: Set environment variables
set USE_TRANSLATIONS=true

:: Run the horoscope generator
python daily_horoscope_replace.py

echo Done!
pause
