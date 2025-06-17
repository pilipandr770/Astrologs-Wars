#!/bin/bash
# build_render.sh - Run during the build phase on Render.com

echo "=== STARTING BUILD PROCESS ==="

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Make scripts executable
echo "Making scripts executable..."
chmod +x prestart.sh
chmod +x *.py
chmod +x *.sh

# Create the root wsgi.py file if it doesn't exist
echo "Ensuring wsgi.py exists in root directory..."
if [ ! -f wsgi.py ]; then
    echo "Creating wsgi.py in the root directory..."
    cat > wsgi.py << 'EOF'
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File for production launch of the application through the Gunicorn WSGI server.
"""

import os
import sys

# Print database connection information (for debugging)
db_url = os.environ.get("DATABASE_URL", "Not set")
print(f"DATABASE_URL: {db_url if 'Not set' in db_url else db_url.split('@')[0] + '@....'}")

try:
    # Create the Flask application
    from app import create_app, db
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
EOF
fi

echo "=== CHECKING DATABASE CONFIGURATION ==="
if [[ -z "${DATABASE_URL}" ]]; then
    echo "WARNING: DATABASE_URL is not set"
else
    # Extract database details from DATABASE_URL
    # Format: postgresql://username:password@hostname:port/database
    DB_URL_SAFE=$(echo $DATABASE_URL | sed 's/\/\/[^:]*:\([^@]*\)@/\/\/[username]:[password]@/g')
    echo "Database URL: $DB_URL_SAFE"
    
    # Parse connection details
    DB_USER=$(echo $DATABASE_URL | sed -e 's/^postgresql:\/\/\([^:]*\):.*$/\1/')
    DB_PASS=$(echo $DATABASE_URL | sed -e 's/^postgresql:\/\/[^:]*:\([^@]*\)@.*$/\1/')
    DB_HOST=$(echo $DATABASE_URL | sed -e 's/^postgresql:\/\/[^@]*@\([^:]*\):.*$/\1/')
    DB_PORT=$(echo $DATABASE_URL | sed -e 's/^postgresql:\/\/[^:]*:[^@]*@[^:]*:\([^/]*\)\/.*$/\1/')
    DB_NAME=$(echo $DATABASE_URL | sed -e 's/^postgresql:\/\/[^:]*:[^@]*@[^:]*:[^/]*\/\(.*\)$/\1/')
    
    echo "Host: $DB_HOST, Port: $DB_PORT, Database: $DB_NAME"
    
    # Try to connect to the default postgres database and create our database if it doesn't exist
    echo "Checking if database exists and creating it if needed..."
    PGPASSWORD="$DB_PASS" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres -c "CREATE DATABASE $DB_NAME;" || echo "Database already exists or couldn't be created"
    
    echo "Testing database connection..."
    # Test database connection
    python -c "
import os
import sys
from sqlalchemy import create_engine, text
try:
    engine = create_engine(os.environ.get('DATABASE_URL'), connect_args={'connect_timeout': 5})
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
        print('Database connection successful!')
except Exception as e:
    print(f'Database connection failed: {str(e)}')
    sys.exit(0)  # Don't fail build on DB error
"
fi

echo "=== BUILD PROCESS COMPLETED ==="
