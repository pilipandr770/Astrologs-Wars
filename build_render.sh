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
    cp app/wsgi.py wsgi.py || echo "Error copying wsgi.py file"
fi

echo "=== CHECKING DATABASE CONFIGURATION ==="
if [[ -z "${DATABASE_URL}" ]]; then
    echo "WARNING: DATABASE_URL is not set"
else
    # Hide password in logs
    DB_URL_SAFE=$(echo $DATABASE_URL | sed 's/\/\/[^:]*:\([^@]*\)@/\/\/[username]:[password]@/g')
    echo "Database URL: $DB_URL_SAFE"
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
