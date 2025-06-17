#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File for production launch of the application through the Gunicorn WSGI server.
"""

import os
import sys
from app import create_app, db

# Print database connection information (for debugging)
db_url = os.environ.get("DATABASE_URL", "Not set")
print(f"DATABASE_URL: {db_url if 'Not set' in db_url else db_url.split('@')[0] + '@....'}")

try:
    # Create the Flask application
    app = create_app()
    
    # Ensure the database exists and has the required tables
    with app.app_context():
        print("Checking database connection and tables...")
        try:
            # Try to create all tables if they don't exist
            db.create_all()
            print("Database tables created or verified successfully")
            
            # Check if we need to create an admin user
            from app.models import User
            if not User.query.filter_by(username='admin').first():
                print("Creating default admin user...")
                admin = User(username='admin', is_admin=True)
                # Generate a password hash
                from werkzeug.security import generate_password_hash
                admin.password_hash = generate_password_hash('admin123')
                db.session.add(admin)
                db.session.commit()
                print("Admin user created! Username: admin, Password: admin123")
            
            # Start the blog automation scheduler if enabled
            from app.blog_automation.models import AutopostingSchedule
            from app.blog_automation.scheduler import get_scheduler
            
            schedule = AutopostingSchedule.query.filter_by(is_active=True).first()
            if schedule:
                scheduler = get_scheduler(app)
                if scheduler:
                    scheduler.start()
                    print("Blog automation scheduler started in WSGI mode")
            
        except Exception as e:
            print(f"Database initialization error: {str(e)}")
            # Don't exit - continue app startup even if DB fails
    
except Exception as e:
    print(f"Application initialization error: {str(e)}")
    sys.exit(1)

if __name__ == "__main__":
    app.run()
