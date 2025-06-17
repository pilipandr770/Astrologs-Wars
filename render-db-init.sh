#!/bin/bash
# render-db-init.sh - Script to initialize database on Render

echo "Starting database initialization for Render deployment..."

# Get the current directory
CURRENT_DIR=$(pwd)
echo "Current directory: $CURRENT_DIR"

# Check if .env file exists
if [ -f .env ]; then
  echo "Found .env file. Checking database URL..."
  # Source env vars from .env file
  set -a
  . ./.env
  set +a
  
  # Check if DATABASE_URL is set and is PostgreSQL
  if [[ -z "$DATABASE_URL" ]]; then
    echo "ERROR: DATABASE_URL is not set in .env file."
    exit 1
  elif [[ ! "$DATABASE_URL" == postgresql://* ]]; then
    echo "ERROR: DATABASE_URL must be a PostgreSQL URL starting with postgresql://"
    exit 1
  else
    echo "PostgreSQL DATABASE_URL is properly configured."
  fi
else
  echo "WARNING: .env file not found, relying on environment variables."
  
  # Check environment variables
  if [[ -z "$DATABASE_URL" ]]; then
    echo "ERROR: DATABASE_URL environment variable is not set."
    exit 1
  elif [[ ! "$DATABASE_URL" == postgresql://* ]]; then
    echo "ERROR: DATABASE_URL must be a PostgreSQL URL starting with postgresql://"
    exit 1
  else
    echo "PostgreSQL DATABASE_URL is properly configured."
  fi
fi

# Install required packages if needed
echo "Checking requirements..."
pip install -r requirements.txt

# Run the database initialization script
echo "Running database initialization script..."
python initialize_render_db.py

# Check if we want to run SQL directly
if [ "$1" == "--sql" ]; then
  echo "Running SQL initialization script via psql..."
  
  # Extract DB connection info from DATABASE_URL
  if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL not set"
    exit 1
  fi
  
  # Parse the PostgreSQL URL
  # Format: postgresql://username:password@hostname:port/database
  DB_USER=$(echo $DATABASE_URL | sed -e 's/^postgresql:\/\/\([^:]*\):.*$/\1/')
  DB_PASS=$(echo $DATABASE_URL | sed -e 's/^postgresql:\/\/[^:]*:\([^@]*\)@.*$/\1/')
  DB_HOST=$(echo $DATABASE_URL | sed -e 's/^postgresql:\/\/[^@]*@\([^:]*\):.*$/\1/')
  DB_PORT=$(echo $DATABASE_URL | sed -e 's/^postgresql:\/\/[^:]*:[^@]*@[^:]*:\([^/]*\)\/.*$/\1/')
  DB_NAME=$(echo $DATABASE_URL | sed -e 's/^postgresql:\/\/[^:]*:[^@]*@[^:]*:[^/]*\/\(.*\)$/\1/')
  
  # Execute SQL script using environment variables
  PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f create_database.sql
  
  echo "SQL initialization complete."
else
  echo "If you want to run the SQL script directly, use: ./render-db-init.sh --sql"
fi

echo "Database initialization process complete!"
