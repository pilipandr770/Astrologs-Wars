#!/bin/bash

echo "==================================================="
echo "Запуск автоматической генерации гороскопов"
echo "==================================================="
echo

# Активируем виртуальное окружение, если оно есть
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Виртуальное окружение активировано"
else
    echo "Виртуальное окружение не найдено, используем системный Python"
fi

# Проверяем наличие пакета schedule
pip show schedule > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Устанавливаем необходимые пакеты..."
    pip install schedule
fi

# Запускаем планировщик
echo
echo "Запускаем планировщик гороскопов..."
echo "Генерация будет выполняться каждый день в 7:00 утра."
echo "Для прекращения работы нажмите Ctrl+C."
echo

python schedule_horoscopes.py

# При выходе деактивируем виртуальное окружение
if [ -f "venv/bin/deactivate" ]; then
    deactivate
fi
