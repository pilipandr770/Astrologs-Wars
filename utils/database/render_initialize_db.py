#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Render database initialization script.
This script is designed to be run inside the Render environment to set up the database.
It will:
1. Create all tables defined in SQLAlchemy models
2. Create a default admin user
3. Check for database connectivity issues

Usage:
python render_initialize_db.py
"""

import os
import sys
from sqlalchemy import text

print("=== STARTING DATABASE INITIALIZATION ===")

# Make sure the DATABASE_URL is set
db_url = os.environ.get("DATABASE_URL")
if not db_url:
    print("ERROR: DATABASE_URL environment variable is not set")
    sys.exit(1)

# Print database connection information (for debugging)
print(f"DATABASE_URL: {db_url.split('@')[0] + '@....'}")

try:
    # Import Flask app and database
    from app import create_app, db
    app = create_app()
    
    # Test raw database connection
    print("Testing raw database connection...")
    with db.engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        if result:
            print("✅ Raw database connection successful")
        else:
            print("❌ Raw database connection failed")
    
    # Initialize the database within the application context
    with app.app_context():
        print("Creating all database tables...")
        db.create_all()
        print("✅ Database tables created successfully")
        
        # List all tables to confirm they were created
        print("\nVerifying created tables:")
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        for table in tables:
            print(f"  - {table}")
        
        # Create admin user if it doesn't exist
        from app.models import User
        if not User.query.filter_by(username='admin').first():
            print("\nCreating default admin user...")
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            from werkzeug.security import generate_password_hash
            admin.password_hash = generate_password_hash('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created successfully")
            print("   Username: admin")
            print("   Password: admin123")
        else:
            print("\n✅ Admin user already exists")
        
        # Initialize blog automation scheduler if needed
        try:
            from app.blog_automation.models import AutopostingSchedule
            schedules = AutopostingSchedule.query.filter_by(is_active=True).all()
            print(f"\nFound {len(schedules)} active blog automation schedules")
        except Exception as e:
            print(f"Warning: Could not check blog automation schedules: {str(e)}")
        
        print("\n=== DATABASE INITIALIZATION COMPLETED SUCCESSFULLY ===")
        
except Exception as e:
    print(f"❌ ERROR: Database initialization failed: {str(e)}")
    sys.exit(1)
