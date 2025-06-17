#!/bin/bash
# quick_fix_db.sh - One-command fix for the missing database issue

echo "🔧 QUICK FIX: Creating astro_blog_db database..."

# Database connection details
DB_USER="ittoken_db_user"
DB_PASS="Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42"
DB_HOST="dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com"
DB_PORT="5432"

echo "Connecting to PostgreSQL server..."

# Create the database if it doesn't exist
PGPASSWORD="$DB_PASS" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres << EOF
-- Create astro_blog_db database
SELECT 'CREATE DATABASE astro_blog_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'astro_blog_db')\gexec

-- List all databases to confirm
\l
EOF

echo "✅ Database creation complete!"
echo ""
echo "🚀 Now redeploy your Render service. The deployment should succeed."
echo ""
echo "If you want to create tables manually, run:"
echo "   psql \"postgresql://$DB_USER:$DB_PASS@$DB_HOST/$DB_PORT/astro_blog_db\""
echo "   Then run the SQL commands from create_database.sql"
