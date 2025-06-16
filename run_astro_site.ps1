Write-Output "Запуск астрологического сайта..."
Write-Output ""
Write-Output "Настройка переменных окружения..."
$env:FLASK_APP="app.run"
$env:FLASK_ENV="development"
Write-Output ""
Write-Output "Запуск Flask-сервера..."
Write-Output ""
flask run --host=0.0.0.0 --port=5000
