#!/usr/bin/env python3
# render_setup_db.py - Script to create all necessary database tables on Render

import os
from dotenv import load_dotenv
load_dotenv()

# Print current database connection info (without password)
db_url = os.environ.get("DATABASE_URL", "")
if db_url:
    # Hide password for security
    safe_db_url = db_url.replace(":", ":*****@", 1) if ":" in db_url else db_url
    print(f"Using database: {safe_db_url}")
else:
    print("DATABASE_URL environment variable is not set!")
    exit(1)

# Create database tables
from app import create_app, db
from app.models import (User, Block, PaymentMethod, Payment, Settings, Category, 
                       Product, ProductImage, Cart, CartItem, Order, OrderItem, 
                       BlogBlock, ImageStorage)
from app.blog_automation.models import (BlogTopic, AutopostingSchedule, 
                                       ContentGenerationLog)

app = create_app()

with app.app_context():
    print("Creating all database tables...")
    db.create_all()
    
    # Check if admin user exists and create if not
    if not User.query.filter_by(username='admin').first():
        print("Creating admin user...")
        admin = User(username='admin', is_admin=True)
        # Generate a password hash (this is not secure for production, you'd need to hash it properly)
        from werkzeug.security import generate_password_hash
        admin.password_hash = generate_password_hash('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created! Username: admin, Password: admin123")
        print("IMPORTANT: Please change this password immediately after first login!")
    else:
        print("Admin user already exists")
    
    # Create default settings
    if not Settings.query.first():
        print("Creating default settings...")
        settings = Settings(
            facebook="https://facebook.com/",
            instagram="https://instagram.com/", 
            telegram="https://t.me/",
            email="contact@example.com"
        )
        db.session.add(settings)
        db.session.commit()
        print("Default settings created")
    
    # Create default autoposting schedule
    if not AutopostingSchedule.query.first():
        print("Creating default blog posting schedule...")
        schedule = AutopostingSchedule(
            is_active=False,
            days_of_week="1,3,5", 
            posting_time="12:00"
        )
        db.session.add(schedule)
        db.session.commit()
        print("Default posting schedule created")
    
    # Create test blog topic if none exists
    if not BlogTopic.query.first():
        print("Creating test blog topic...")
        test_topic = BlogTopic(
            title="Welcome to Astrology Blog",
            title_ua="Ласкаво просимо до Астрологічного блогу",
            title_en="Welcome to Astrology Blog",
            title_de="Willkommen im Astrologie-Blog",
            title_ru="Добро пожаловать в Астрологический блог",
            description_ua="Перший тестовий допис",
            description_en="First test post",
            description_de="Erster Testbeitrag",
            description_ru="Первый тестовый пост",
            status="active"
        )
        db.session.add(test_topic)
        db.session.commit()
        print("Test blog topic created")
    
    print("\nDatabase setup complete! All necessary tables have been created.")
    
    # List all tables in the database
    print("\nAvailable tables in the database:")
    for table in db.metadata.tables.items():
        print(f"- {table[0]}")
