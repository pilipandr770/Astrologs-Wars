#!/usr/bin/env python3
"""
Скрипт для ручной инициализации базы данных в терминале Render
Используйте этот скрипт если автоматическая инициализация не сработала
"""

import os
import sys

# Добавляем текущую директорию в path
sys.path.insert(0, '/opt/render/project/src')

def init_database():
    print("🚀 ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ...")
    
    try:
        # Очистка DATABASE_URL от лишних символов
        db_url = os.environ.get("DATABASE_URL")
        if db_url:
            db_url_clean = db_url.strip()
            if db_url != db_url_clean:
                print(f"🔧 Исправлен DATABASE_URL: {repr(db_url)} -> {repr(db_url_clean)}")
                os.environ["DATABASE_URL"] = db_url_clean
            print(f"🔗 DATABASE_URL: {db_url_clean[:60]}...")
        
        # Импортируем приложение
        from app import create_app, db
        
        print("📝 Создание приложения...")
        app = create_app()
        
        with app.app_context():
            print("🗄️ Создание всех таблиц...")
            
            # Создание таблиц
            db.create_all()
            print("✅ Таблицы созданы успешно!")
            
            # Проверка созданных таблиц
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Созданные таблицы ({len(tables)}): {', '.join(tables)}")
            
            # Создание администратора
            from app.models import User
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                print("👤 Создание администратора...")
                from werkzeug.security import generate_password_hash
                
                admin = User(
                    username='admin',
                    email='admin@astro.com',
                    is_admin=True
                )
                admin.password_hash = generate_password_hash('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✅ Администратор создан!")
                print("📧 Username: admin")
                print("🔐 Password: admin123")
            else:
                print("👤 Администратор уже существует")
            
            # Проверка количества пользователей
            user_count = User.query.count()
            print(f"👥 Общее количество пользователей: {user_count}")
            
            print("🎉 ИНИЦИАЛИЗАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
            
    except Exception as e:
        print(f"❌ ОШИБКА: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    init_database()
