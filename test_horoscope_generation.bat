@echo off
REM Batch script to test horoscope content generation

echo Testing horoscope content generation...

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated
) else if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo No virtual environment found
)

REM Run the test script
echo Running horoscope generation test...
python test_horoscope_generation.py

if %ERRORLEVEL% EQU 0 (
    echo Horoscope generation test completed successfully!
) else (
    echo Horoscope generation test failed with exit code: %ERRORLEVEL%
)

REM If using virtual environment, deactivate it
if defined VIRTUAL_ENV (
    call deactivate
    echo Virtual environment deactivated
)

echo Press any key to exit...
pause > nul
