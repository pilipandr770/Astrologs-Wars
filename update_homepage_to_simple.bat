@echo off
REM Script for updating the homepage to a simple project info page (Windows)

echo === Updating Homepage to Simple Project Info ===
python update_homepage_to_simple.py

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
