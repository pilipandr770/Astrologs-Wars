Write-Host "Running enhanced daily horoscope generator with improved images..." -ForegroundColor Green

# Проверяем существование файла перед запуском
if (Test-Path -Path "daily_horoscope_replace.py") {
    # Запускаем скрипт генерации гороскопов
    python daily_horoscope_replace.py
    Write-Host "Done." -ForegroundColor Green
}
else {
    Write-Host "Error: File 'daily_horoscope_replace.py' not found!" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)"
    Write-Host "Python files in current directory:"
    Get-ChildItem -Filter "*.py" | ForEach-Object { Write-Host "  - $($_.Name)" }
}

Read-Host -Prompt "Press Enter to exit"
