#!/bin/bash
# Скрипт для запуска трансформации сайта

# Создаем резервную копию БД
cp instance/app.db instance/app.db.backup

# Запускаем скрипты трансформации
echo "Удаляем функциональность токенов..."
python remove_token_functionality.py

echo "Улучшаем автоматизацию блога..."
python enhance_blog_automation.py

echo "Трансформация успешно завершена!"
echo "Рекомендуется перезапустить приложение."
