# Database Setup for Render Deployment

This document explains how to set up the database for deployment on Render.com.

## Prerequisites

1. A Render.com account
2. A PostgreSQL database service on Render
3. The correct PostgreSQL connection string in your `.env` file

## Database Schema

The application requires several tables to function properly:

- Users and authentication
- Content blocks
- Blog automation system
- Payment processing
- Products and shop
- Token/blockchain functionality
- And more

## Setup Options

You have three methods to set up the database:

### Option 1: Use SQLAlchemy's create_all() (Recommended for new deployments)

This approach uses SQLAlchemy's built-in schema generation capability.

1. Make sure your `DATABASE_URL` is correctly set in `.env`:
   ```
   DATABASE_URL=postgresql://username:password@host.frankfurt-postgres.render.com:5432/database_name
   ```

2. Run the database initialization script:
   ```bash
   # On Linux/macOS
   ./render-db-init.sh
   
   # On Windows PowerShell
   .\render-db-init.ps1
   ```

### Option 2: Direct SQL Execution

If you prefer to run raw SQL statements:

1. Make sure your `DATABASE_URL` is set correctly.

2. Run the SQL initialization script:
   ```bash
   # On Linux/macOS
   ./render-db-init.sh --sql
   
   # On Windows PowerShell
   .\render-db-init.ps1 --sql
   ```

### Option 3: Manual Setup

If you need more control, you can manually execute the SQL:

1. Connect to your PostgreSQL database using a client like pgAdmin or using the Render dashboard.

2. Execute the SQL statements from `create_database.sql`.

## Setting Up Migrations with Flask-Migrate (For Future Changes)

For future database changes, consider setting up Flask-Migrate (Alembic):

1. Install Flask-Migrate:
   ```bash
   pip install Flask-Migrate
   ```

2. Add to your requirements.txt:
   ```
   Flask-Migrate==4.0.5
   ```

3. Modify `app/__init__.py` to add migration support:
   ```python
   from flask_migrate import Migrate
   
   # After creating the app and initializing db
   migrate = Migrate(app, db)
   ```

4. Initialize the migration repository:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. For future changes, create new migrations:
   ```bash
   flask db migrate -m "Add new field"
   flask db upgrade
   ```

## Troubleshooting

### Connection Issues

- Ensure the host includes the region suffix: `host.frankfurt-postgres.render.com`
- Check that the database user has proper permissions
- Verify the database exists on your PostgreSQL instance

### Schema Issues

- If you see errors about missing columns, make sure you're using the latest schema
- Check that all tables are created properly with `\dt` in psql

## Important Notes

- Make sure to properly secure your database connection string
- The database URL should be set in the Render environment variables
- Regular backups are recommended
