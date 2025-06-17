#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Файл для продакшн-запуска приложения через Gunicorn WSGI-сервер.
"""

import os
from app import create_app

# КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ: Очистка DATABASE_URL от лишних символов
db_url = os.environ.get("DATABASE_URL")
if db_url:
    db_url_clean = db_url.strip()
    if db_url != db_url_clean:
        print(f"ИСПРАВЛЕН DATABASE_URL whitespace: {repr(db_url)} -> {repr(db_url_clean)}")
        os.environ["DATABASE_URL"] = db_url_clean
    print(f"DATABASE_URL: {db_url_clean[:50]}...")

app = create_app()

# АВТОМАТИЧЕСКОЕ СОЗДАНИЕ ТАБЛИЦ ПРИ ДЕПЛОЕ
with app.app_context():
    try:
        from app import db
        
        print("🚀 Проверка базы данных и создание таблиц...")
        
        # Создаем все таблицы
        db.create_all()
        print("✅ Таблицы базы данных созданы/проверены успешно")
        
        # Создаем администратора по умолчанию
        from app.models import User
        if not User.query.filter_by(username='admin').first():
            print("👤 Создание администратора по умолчанию...")
            from werkzeug.security import generate_password_hash
            admin = User(
                username='admin',
                email='admin@astro.com',
                is_admin=True
            )
            admin.password_hash = generate_password_hash('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Администратор создан! Username: admin, Password: admin123")
        else:
            print("👤 Администратор уже существует")
            
        # Запуск планировщика блогов (если необходимо)
        try:
            from app.blog_automation.models import AutopostingSchedule
            from app.blog_automation.scheduler import get_scheduler
            
            schedule = AutopostingSchedule.query.filter_by(is_active=True).first()
            if schedule:
                scheduler = get_scheduler(app)
                if scheduler:
                    scheduler.start()
                    print("📅 Планировщик автоматизации блогов запущен")
        except Exception as scheduler_error:
            print(f"⚠️ Ошибка запуска планировщика: {str(scheduler_error)}")
        
        print("🎉 Инициализация базы данных завершена успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка инициализации базы данных: {str(e)}")
        import traceback
        traceback.print_exc()
        # Не выходим из приложения - продолжаем запуск

if __name__ == "__main__":
    app.run()
