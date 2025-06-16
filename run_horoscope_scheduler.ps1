# PowerShell скрипт для запуска автоматической генерации гороскопов

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Запуск автоматической генерации гороскопов" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

# Активируем виртуальное окружение, если оно есть
if (Test-Path "venv\Scripts\Activate.ps1") {
    . .\venv\Scripts\Activate.ps1
    Write-Host "Виртуальное окружение активировано" -ForegroundColor Green
} else {
    Write-Host "Виртуальное окружение не найдено, используем системный Python" -ForegroundColor Yellow
}

# Проверяем наличие пакета schedule
$scheduleInstalled = python -c "import pkgutil; print(pkgutil.find_loader('schedule') is not None)" 2>$null
if ($scheduleInstalled -ne "True") {
    Write-Host "Устанавливаем необходимые пакеты..." -ForegroundColor Yellow
    pip install schedule
}

# Запускаем планировщик
Write-Host ""
Write-Host "Запускаем планировщик гороскопов..." -ForegroundColor Green
Write-Host "Генерация будет выполняться каждый день в 7:00 утра." -ForegroundColor Cyan
Write-Host "Для прекращения работы нажмите Ctrl+C." -ForegroundColor Cyan
Write-Host ""

python schedule_horoscopes.py

# При выходе деактивируем виртуальное окружение
if ($env:VIRTUAL_ENV) {
    deactivate
}
