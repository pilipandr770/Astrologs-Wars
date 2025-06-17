#!/usr/bin/env python3
# initialize_render_db.py - Script to initialize database on Render

from dotenv import load_dotenv
load_dotenv()

import os
import sys

print("Database URL:", os.environ.get("DATABASE_URL"))

if not os.environ.get("DATABASE_URL") or not os.environ.get("DATABASE_URL").startswith("postgresql://"):
    print("ERROR: Please set a valid DATABASE_URL environment variable for PostgreSQL.")
    print("It should start with postgresql://")
    sys.exit(1)

print("Initializing database...")

from app import create_app, db
from app.models import (
    User, Block, PaymentMethod, Payment, Settings, Category, Product, ProductImage,
    Cart, CartItem, Order, OrderItem, Token, Airdrop, AirdropParticipation,
    TokenSale, TokenPurchase, DaoProposal, DaoVote, BlogBlock, ImageStorage
)
from app.blog_automation.models import (
    BlogTopic, AutopostingSchedule, ContentGenerationLog
)

def setup_database():
    """Create database tables and initial data"""
    app = create_app()

    with app.app_context():
        # Create all tables
        print("Creating all tables...")
        db.create_all()
        
        # Check if admin user exists and create if not
        if not User.query.filter_by(username='admin').first():
            print("Creating admin user...")
            admin = User(username='admin', is_admin=True)
            admin.password_hash = 'pbkdf2:sha256:260000$your-hashed-password'  # Should be replaced with a proper hashed password
            db.session.add(admin)
            db.session.commit()
            print("Admin user created!")
        
        # Create default settings if needed
        if not Settings.query.first():
            print("Creating default settings...")
            settings = Settings(
                facebook="https://www.facebook.com/",
                instagram="https://www.instagram.com/",
                telegram="https://t.me/",
                email="contact@example.com"
            )
            db.session.add(settings)
            db.session.commit()
            print("Default settings created!")
        
        # Create default autoposting schedule if needed
        if not AutopostingSchedule.query.first():
            print("Creating default blog autoposting schedule...")
            schedule = AutopostingSchedule(
                is_active=False,  # Default to inactive until explicitly enabled
                days_of_week="1,3,5",  # Mon, Wed, Fri
                posting_time="12:00"
            )
            db.session.add(schedule)
            db.session.commit()
            print("Default autoposting schedule created!")
            
        # You can add more initial data as needed
        
        print("Database initialization complete!")
        print("All tables were successfully created.")

if __name__ == "__main__":
    setup_database()
