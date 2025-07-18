# app/__init__.py
import os
from flask import Flask, g, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from pathlib import Path

# Загрузка переменных из .env файла
try:
    from dotenv import load_dotenv
    # Попытка загрузки .env файла из корневой директории проекта
    env_path = Path(__file__).resolve().parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Переменные окружения загружены из {env_path}")
except ImportError:
    print("python-dotenv не установлен, переменные окружения должны быть настроены вручную")

db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Будь ласка, увійдіть в систему для доступу до цієї сторінки.'
    babel.init_app(app)
    
    # Create database tables if they don't exist
    from .models import Block  # Import Block to ensure it's registered with SQLAlchemy
    with app.app_context():
        db.create_all()
        print("Database tables created with db.create_all()")
        
        # Start blog automation scheduler if enabled
        from app.blog_automation.models import AutopostingSchedule
        from app.blog_automation.scheduler import get_scheduler
        
        try:
            schedule = AutopostingSchedule.query.filter_by(is_active=True).first()
            if schedule:
                scheduler = get_scheduler(app)
                if scheduler:
                    scheduler.start()
                    print("Blog automation scheduler started")
        except Exception as e:
            print(f"Error starting blog automation scheduler: {str(e)}")
    
    # Ensure uploads directory exists
    uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    print(f"Ensuring uploads directory exists: {uploads_dir}")
    
    # Create a .gitkeep file to preserve directory structure
    gitkeep_path = os.path.join(uploads_dir, '.gitkeep')
    if not os.path.exists(gitkeep_path):
        with open(gitkeep_path, 'w') as f:
            f.write('# This file ensures the uploads directory is tracked by git\n')

    # Register custom filters
    from app.utils.filters import register_filters
    register_filters(app)
    
    # Зберігати вибір мови в сесії
    @app.before_request
    def set_lang():
        lang = request.args.get('lang')
        if lang:
            session['lang'] = lang
        g.lang = session.get('lang', None)
    
    # Підключення blueprint'ів
    from app.main.routes import main
    from app.admin.routes import admin
    from app.shop.routes import shop
    from .assist import assist_bp
    from .blog import blog_bp
    from .blog_automation import blog_automation_bp
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(shop)
    app.register_blueprint(assist_bp)
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(blog_automation_bp)

    # Регистрируем template helper функции как глобальные в Jinja2
    from app.main.routes import (
        get_block_title, get_block_content, get_category_name, get_product_name, 
        get_product_description
    )
    
    app.jinja_env.globals.update(
        get_block_title=get_block_title,
        get_block_content=get_block_content,
        get_category_name=get_category_name,
        get_product_name=get_product_name,
        get_product_description=get_product_description
    )

    return app

# Babel локалізатор
@babel.localeselector
def get_locale():
    from flask import request, session
    lang = request.args.get('lang')
    if lang:
        session['lang'] = lang
        return lang
    if 'lang' in session:
        return session['lang']
    return request.accept_languages.best_match(['uk', 'en', 'de', 'ru'])

from app.models import User

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    """Повертає користувача для Flask-Login за id"""
    return User.query.get(int(user_id))
