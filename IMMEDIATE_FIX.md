# IMMEDIATE FIX FOR DEPLOYMENT ERROR

## Problem
Your Render deployment is failing with this error:
```
FATAL: database "astro_blog_db" does not exist
```

## Solution
The database `astro_blog_db` needs to be created on your PostgreSQL server.

## Quick Fix Options

### Option 1: Use psql command (if you have PostgreSQL client installed)

Run this command in your terminal:

```bash
psql "postgresql://ittoken_db_user:Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42@dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com/postgres" -c "CREATE DATABASE astro_blog_db;"
```

### Option 2: Use Render's Web Shell

1. Go to your Render service dashboard
2. Click on "Shell" tab
3. Run: `bash quick_fix_db.sh`

### Option 3: Manual Steps via psql

1. Connect to the default postgres database:
```bash
psql "postgresql://ittoken_db_user:Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42@dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com/postgres"
```

2. Create the database:
```sql
CREATE DATABASE astro_blog_db;
```

3. Verify it was created:
```sql
\l
```

4. Exit psql:
```sql
\q
```

### Option 4: Temporary Workaround

If you can't create the database, temporarily change your `render.yaml` to use the existing `postgres` database:

Change this line in render.yaml:
```yaml
value: "postgresql://ittoken_db_user:Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42@dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com/astro_blog_db"
```

To this:
```yaml
value: "postgresql://ittoken_db_user:Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42@dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com/postgres"
```

## After Creating the Database

1. Push your changes to the repository
2. Trigger a new deployment on Render
3. The deployment should now succeed

## Verification

To verify the database was created, connect and list all databases:
```bash
psql "postgresql://ittoken_db_user:Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42@dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com/postgres" -c "\l"
```

You should see `astro_blog_db` in the list.

---

**Status: READY TO DEPLOY**

Once the database is created, your Render deployment will work correctly. The application will automatically create the required tables when it starts.
