@echo off
echo ===================================================
echo Запуск автоматической генерации гороскопов
echo ===================================================
echo.

:: Активируем виртуальное окружение, если оно есть
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Виртуальное окружение активировано
) else (
    echo Виртуальное окружение не найдено, используем системный Python
)

:: Проверяем наличие пакета schedule
pip show schedule >nul 2>&1
if %errorlevel% neq 0 (
    echo Устанавливаем необходимые пакеты...
    pip install schedule
)

:: Запускаем планировщик
echo.
echo Запускаем планировщик гороскопов...
echo Генерация будет выполняться каждый день в 7:00 утра.
echo Для прекращения работы нажмите Ctrl+C.
echo.
python schedule_horoscopes.py

:: Деактивируем виртуальное окружение при выходе
if exist venv\Scripts\deactivate.bat (
    call venv\Scripts\deactivate.bat
)

pause
