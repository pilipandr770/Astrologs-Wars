@echo off
echo Starting translation fix script...
python fix_translations.py
if %ERRORLEVEL% EQU 0 (
    echo Translation fix completed successfully!
) else (
    echo Translation fix failed with error code %ERRORLEVEL%
)
pause
