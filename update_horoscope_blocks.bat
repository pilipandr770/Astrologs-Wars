@echo off
REM Script for updating horoscope blocks styling (Windows)

echo === Updating Horoscope Blocks Styling ===
python update_horoscope_blocks_visual.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo === Success! ===
    echo Restart your application to see the changes.
    echo You can use run_astro_site.bat to restart.
) else (
    echo.
    echo === Error occurred ===
    echo Please check the output above for details.
)

pause
