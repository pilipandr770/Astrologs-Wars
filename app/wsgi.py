#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Файл для продакшн-запуска додатку через Gunicorn WSGI-сервер.
"""

import os
from app import create_app

# CRITICAL FIX: Clean DATABASE_URL from any whitespace/newlines
db_url = os.environ.get("DATABASE_URL")
if db_url:
    db_url_clean = db_url.strip()
    if db_url != db_url_clean:
        print(f"FIXED DATABASE_URL whitespace: {repr(db_url)} -> {repr(db_url_clean)}")
        os.environ["DATABASE_URL"] = db_url_clean
    print(f"DATABASE_URL: {db_url_clean[:50]}...")

app = create_app()

# АВТОМАТИЧЕСКОЕ СОЗДАНИЕ ТАБЛИЦ ПРИ ДЕПЛОЕ
with app.app_context():
    try:
        from app import db
        
        print("🚀 Checking database and creating tables...")
        
        # Создаем все таблицы
        db.create_all()
        print("✅ Database tables created/verified successfully")
        
        # Создаем администратора по умолчанию
        from app.models import User
        if not User.query.filter_by(username='admin').first():
            print("👤 Creating default admin user...")
            from werkzeug.security import generate_password_hash
            admin = User(
                username='admin',
                email='admin@astro.com',
                is_admin=True
            )
            admin.password_hash = generate_password_hash('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created! Username: admin, Password: admin123")
        else:
            print("👤 Admin user already exists")
            
        # Запуск планировщика блогов (если необходимо)
        from app.blog_automation.models import AutopostingSchedule
        from app.blog_automation.scheduler import get_scheduler
        
        schedule = AutopostingSchedule.query.filter_by(is_active=True).first()
        if schedule:
            scheduler = get_scheduler(app)
            if scheduler:
                scheduler.start()
                print("📅 Blog automation scheduler started")
        
        print("🎉 Database initialization completed successfully!")
        
    except Exception as e:
        print(f"❌ Database initialization error: {str(e)}")
        import traceback
        traceback.print_exc()
        # Не выходим из приложения - продолжаем запуск
            if scheduler:
                scheduler.start()
                print("Blog automation scheduler started in WSGI mode")
    except Exception as e:
        print(f"Error starting blog automation scheduler in WSGI mode: {str(e)}")

if __name__ == "__main__":
    app.run()
