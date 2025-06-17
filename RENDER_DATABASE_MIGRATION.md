# URGENT FIX: Database "astro_blog_db" Does Not Exist

## Immediate Solution

Your deployment is failing because the `astro_blog_db` database doesn't exist on your PostgreSQL server. Here's how to fix it immediately:

### Option 1: Create the Database Manually (Recommended)

1. **Connect to your PostgreSQL database via psql:**
   ```bash
   psql "postgresql://ittoken_db_user:Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42@dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com/postgres"
   ```

2. **Create the astro_blog_db database:**
   ```sql
   CREATE DATABASE astro_blog_db;
   ```

3. **Connect to the new database and create the required tables:**
   ```bash
   psql "postgresql://ittoken_db_user:Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42@dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com/astro_blog_db"
   ```

4. **Run the table creation script:**
   ```bash
   bash create_and_setup_db.sh
   ```

### Option 2: Use the Render Shell

1. **Go to your Render service dashboard**
2. **Open the "Shell" tab**
3. **Run the database setup script:**
   ```bash
   bash create_and_setup_db.sh
   ```

### Option 3: Temporarily Use a Different Database

Update your `render.yaml` to use the main postgres database temporarily:

```yaml
      - key: DATABASE_URL
        value: "postgresql://ittoken_db_user:Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42@dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com/postgres"
```

Then after the app starts successfully, you can create the astro_blog_db and switch back.

## Why This Is Happening

The error occurs because:
1. Your application expects a database named `astro_blog_db`
2. This database doesn't exist on your PostgreSQL instance
3. SQLAlchemy's `db.create_all()` can't create tables in a non-existent database

## Quick Commands Reference

**Create database manually:**
```sql
-- Connect to default postgres database
\c postgres

-- Create the astro_blog_db database
CREATE DATABASE astro_blog_db;

-- Switch to the new database
\c astro_blog_db

-- Verify you're in the right database
SELECT current_database();
```

After creating the database, your Render deployment should work correctly.

---

# Render Database Migration Guide

This guide will help you migrate your application's database to Render.com.

## Overview

The project uses SQLAlchemy with PostgreSQL for production. The database contains tables for:

- User authentication and management
- Content blocks and site sections
- Blog automation system with scheduling
- E-commerce functionality (products, orders, cart)
- Payment processing
- Multi-language support
- Image storage and management

## Migration Steps

### 1. Set Up PostgreSQL on Render

1. Log in to your Render dashboard
2. Navigate to "New" > "PostgreSQL"
3. Set up your database with appropriate settings:
   - Name: `astrology-db` (or your preferred name)
   - Database: `astrology`
   - User: Render will generate this
   - Version: Use PostgreSQL 14 or newer
   - Region: Choose Frankfurt or the region closest to your users

4. After creation, note the connection string:
   ```
   postgresql://user:password@host.frankfurt-postgres.render.com:5432/database
   ```

### 2. Update Your Environment Variables

1. Set the `DATABASE_URL` in your `.env` file:
   ```
   DATABASE_URL=postgresql://user:password@host.frankfurt-postgres.render.com:5432/database
   ```

2. Ensure the URL includes the region suffix (e.g., `.frankfurt-postgres.render.com`)

### 3. Initialize the Database

Choose one of these methods:

#### Using Python with SQLAlchemy

Run:
```powershell
# On Windows
.\render-db-init.ps1

# On Linux/Mac
./render-db-init.sh
```

This will:
- Verify your database connection
- Create all tables using SQLAlchemy
- Add initial data (admin user, settings)

#### Using Direct SQL Execution

If you prefer to run SQL directly:

```powershell
# On Windows
.\render-db-init.ps1 --sql

# On Linux/Mac
./render-db-init.sh --sql
```

This executes the `create_database.sql` script which contains all table definitions.

### 4. Test the Connection

To verify the database has been set up correctly:

```powershell
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('All tables:', list(map(str, db.metadata.tables)))"
```

You should see a list of all tables.

## Data Migration Considerations

If you have existing data to migrate from SQLite:

1. **Export data** from your SQLite database to CSV files:
   ```sql
   .mode csv
   .output users.csv
   SELECT * FROM user;
   .output blocks.csv
   SELECT * FROM block;
   -- Repeat for each table
   ```

2. **Import data** into PostgreSQL:
   ```sql
   COPY "user" FROM '/path/to/users.csv' WITH CSV;
   COPY block FROM '/path/to/blocks.csv' WITH CSV;
   -- Repeat for each table
   ```

## Regular Backup Strategy

Set up daily backups on Render:

1. In your PostgreSQL service settings, enable daily backups
2. Set a retention policy (e.g., 7 days)

For manual backups:
```bash
pg_dump -U username -h host.frankfurt-postgres.render.com -d dbname > backup_$(date +%Y%m%d).sql
```

## Future Migrations & Schema Updates

For future database schema changes, consider implementing Flask-Migrate:

1. Install: `pip install Flask-Migrate`
2. Initialize: `flask db init`
3. Create migrations: `flask db migrate -m "Description"`
4. Apply migrations: `flask db upgrade`

See `DATABASE_SETUP.md` for detailed instructions on setting up migrations.

## Troubleshooting

### Common Issues

1. **Connection errors**:
   - Ensure the host includes the region suffix (e.g., `.frankfurt-postgres.render.com`)
   - Check that your IP is whitelisted if restrictions are in place
   - Verify credentials are correct

2. **Schema errors**:
   - Run `db.create_all()` again to add any missing tables
   - Check SQLAlchemy model definitions for changes

3. **Performance issues**:
   - Consider adding indexes for frequently queried columns
   - Review query performance with PostgreSQL EXPLAIN

### Getting Help

If you encounter persistent issues:

1. Check Render's PostgreSQL documentation
2. Verify your connection string format
3. Examine PostgreSQL logs in the Render dashboard
4. Contact Render support for database-specific issues

## Next Steps

After successful migration:

1. Update your web service environment variables on Render
2. Test the application thoroughly with the new database
3. Monitor database performance during initial production use
