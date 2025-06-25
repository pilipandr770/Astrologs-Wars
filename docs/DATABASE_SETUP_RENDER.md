# Database Setup Instructions for Render

This document provides step-by-step instructions on how to set up the database for your astrology application on Render.com.

## Database Setup - Already Completed

You have already completed the initial setup:

1. ✅ Connected to the PostgreSQL database on Render
2. ✅ Created the `astro_blog_db` database
3. ✅ Created tables in the `astro_blog_db` database
4. ✅ Added initial data (blog topics)

## Next Steps

### 1. Update the Environment Configuration

Make sure your application's environment variables point to the correct database:

1. On your Render dashboard, go to your web service
2. Go to "Environment" tab
3. Update the `DATABASE_URL` variable to:
   ```
   postgresql://ittoken_db_user:Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42@dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com/astro_blog_db
   ```
4. Save changes and trigger a manual deploy if needed

### 2. Create Remaining Tables

If you haven't already created all the necessary tables, you can:

**Option A: Use the setup script directly on Render**

1. Open the Render shell for your web service
2. Run the setup script:
   ```bash
   bash setup_astro_blog_db.sh
   ```

**Option B: Run the Python script to create tables**

1. Open the Render shell for your web service
2. Run:
   ```bash
   python render_setup_db.py
   ```

### 3. Verify Database Tables

To check that all tables have been created:

1. Connect to the database:
   ```bash
   psql "postgresql://ittoken_db_user:Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42@dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com/astro_blog_db"
   ```

2. List all tables:
   ```sql
   \dt
   ```

3. Check specific tables (e.g., users):
   ```sql
   SELECT * FROM "user";
   ```

## Troubleshooting

### Connection Issues

If you see "database does not exist" errors:

1. Make sure you've created the `astro_blog_db` database
2. Check that the `DATABASE_URL` environment variable points to `astro_blog_db` (not `postgres` or `ittoken_db`)
3. Verify the proper server address is used (`oregon-postgres.render.com`)

### Table Creation Issues

If tables aren't being created:

1. Check for SQL errors in the logs
2. Try running the SQL commands manually:
   ```sql
   CREATE TABLE IF NOT EXISTS "user" (id SERIAL PRIMARY KEY, username VARCHAR(64) UNIQUE, ...);
   ```

### Application Start Failures

If the application fails to start:

1. Check the logs for SQL connection errors
2. Verify that the `wsgi.py` file is in the correct location
3. Try modifying the start command to:
   ```
   gunicorn wsgi:app --preload
   ```

## Additional Notes

- If you need to switch between databases, update the DATABASE_URL environment variable
- For local development, you can continue to use SQLite by leaving SQLALCHEMY_DATABASE_URI in your .env file
- For production, the PostgreSQL database (astro_blog_db) will be used

## Commands Reference

**Connect to database:**
```bash
psql "postgresql://ittoken_db_user:Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42@dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com/astro_blog_db"
```

**List tables:**
```sql
\dt
```

**Check table structure:**
```sql
\d tablename
```

**Create a new table:**
```sql
CREATE TABLE tablename (
    id SERIAL PRIMARY KEY,
    field1 VARCHAR(255),
    field2 TEXT,
    created_at TIMESTAMP DEFAULT now()
);
```
