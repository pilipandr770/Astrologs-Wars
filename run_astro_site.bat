@echo off
echo Запуск астрологического сайта...
echo.
echo Настройка переменных окружения...
set FLASK_APP=app.run
set FLASK_ENV=development
echo.
echo Запуск Flask-сервера...
echo.
flask run --host=0.0.0.0 --port=5000
