# quick_fix_db.ps1 - PowerShell version of the quick database fix

Write-Host "[QUICK FIX] Creating astro_blog_db database..." -ForegroundColor Green

# Database connection details
$DB_USER = "ittoken_db_user"
$DB_PASS = "Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42"
$DB_HOST = "dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com"
$DB_PORT = "5432"

Write-Host "Connecting to PostgreSQL server..." -ForegroundColor Yellow

# Check if psql is available
$psqlCheck = Get-Command "psql" -ErrorAction SilentlyContinue
if ($null -eq $psqlCheck) {
    Write-Host "[ERROR] psql command not found!" -ForegroundColor Red
    Write-Host "Please install PostgreSQL client tools or use the online psql from Render dashboard" -ForegroundColor Yellow
    Write-Host "You can also run this command manually:" -ForegroundColor Cyan
    $connectionString = "postgresql://$DB_USER`:$DB_PASS@$DB_HOST`:$DB_PORT/postgres"
    Write-Host "psql `"$connectionString`" -c `"CREATE DATABASE astro_blog_db;`"" -ForegroundColor White
    exit 1
}

# Set environment variable for password
$env:PGPASSWORD = $DB_PASS

try {
    # Create the database
    $createDbSql = @"
SELECT 'CREATE DATABASE astro_blog_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'astro_blog_db')\gexec
\l
"@

    $createDbSql | psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres

    Write-Host "[SUCCESS] Database creation complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "[NEXT STEP] Now redeploy your Render service. The deployment should succeed." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "If you want to create tables manually, use this connection string:" -ForegroundColor Yellow
    $astroConnectionString = "postgresql://$DB_USER`:$DB_PASS@$DB_HOST`:$DB_PORT/astro_blog_db"
    Write-Host $astroConnectionString -ForegroundColor White
}
catch {
    Write-Host "[ERROR] Failed to create database" -ForegroundColor Red
    Write-Host "Error details: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Try running this command manually:" -ForegroundColor Yellow
    $fallbackConnectionString = "postgresql://$DB_USER`:$DB_PASS@$DB_HOST`:$DB_PORT/postgres"
    Write-Host "psql `"$fallbackConnectionString`" -c `"CREATE DATABASE astro_blog_db;`"" -ForegroundColor White
}
