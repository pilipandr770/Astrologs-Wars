@echo off
REM Скрипт для запуска трансформации сайта

REM Создаем резервную копию БД
echo Создаем резервную копию базы данных...
copy instance\app.db instance\app.db.backup

REM Запускаем скрипты трансформации
echo Удаляем функциональность токенов...
python remove_token_functionality.py

echo Улучшаем автоматизацию блога...
python enhance_blog_automation.py

echo Трансформация успешно завершена!
echo Рекомендуется перезапустить приложение.
