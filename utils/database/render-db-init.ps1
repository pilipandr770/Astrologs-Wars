# render-db-init.ps1 - PowerShell script to initialize database on Render

Write-Host "Starting database initialization for Render deployment..." -ForegroundColor Green

# Check if .env file exists and load it
if (Test-Path -Path ".env") {
    Write-Host "Found .env file. Checking database URL..."
    
    # Load environment variables from .env file
    $envContent = Get-Content ".env" -ErrorAction SilentlyContinue
    foreach ($line in $envContent) {
        if ($line -match '^\s*([^#][^=]+)=(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            # Remove quotes if they exist
            if ($value -match '^"(.*)"$' -or $value -match "^'(.*)'$") {
                $value = $matches[1]
            }
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
    
    # Check if DATABASE_URL is set and is PostgreSQL
    $dbUrl = [Environment]::GetEnvironmentVariable("DATABASE_URL", "Process")
    if ([string]::IsNullOrEmpty($dbUrl)) {
        Write-Host "ERROR: DATABASE_URL is not set in .env file." -ForegroundColor Red
        exit 1
    }
    elseif (-not $dbUrl.StartsWith("postgresql://")) {
        Write-Host "ERROR: DATABASE_URL must be a PostgreSQL URL starting with postgresql://" -ForegroundColor Red
        exit 1
    }
    else {
        Write-Host "PostgreSQL DATABASE_URL is properly configured." -ForegroundColor Green
    }
}
else {
    Write-Host "WARNING: .env file not found, relying on environment variables." -ForegroundColor Yellow
    
    # Check environment variables
    $dbUrl = [Environment]::GetEnvironmentVariable("DATABASE_URL", "Process")
    if ([string]::IsNullOrEmpty($dbUrl)) {
        Write-Host "ERROR: DATABASE_URL environment variable is not set." -ForegroundColor Red
        exit 1
    }
    elseif (-not $dbUrl.StartsWith("postgresql://")) {
        Write-Host "ERROR: DATABASE_URL must be a PostgreSQL URL starting with postgresql://" -ForegroundColor Red
        exit 1
    }
    else {
        Write-Host "PostgreSQL DATABASE_URL is properly configured." -ForegroundColor Green
    }
}

# Install required packages if needed
Write-Host "Checking requirements..." -ForegroundColor Green
pip install -r requirements.txt

# Run the database initialization script
Write-Host "Running database initialization script..." -ForegroundColor Green
python initialize_render_db.py

# Check if we want to run SQL directly
if ($args -contains "--sql") {
    Write-Host "Running SQL initialization script directly..." -ForegroundColor Green
    
    # Check if psql is in the path
    $psqlCheck = Get-Command "psql" -ErrorAction SilentlyContinue
    if ($null -eq $psqlCheck) {
        Write-Host "PostgreSQL client (psql) not found in PATH. Please install PostgreSQL client tools." -ForegroundColor Red
        Write-Host "You can download from: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
        exit 1
    }
    
    # Parse the PostgreSQL URL
    # Format: postgresql://username:password@hostname:port/database
    $dbUrl = [Environment]::GetEnvironmentVariable("DATABASE_URL", "Process")
    if ([string]::IsNullOrEmpty($dbUrl)) {
        Write-Host "ERROR: DATABASE_URL not set" -ForegroundColor Red
        exit 1
    }
    
    try {
        $uri = New-Object System.Uri($dbUrl)
        $userInfo = $uri.UserInfo.Split(":")
        $DB_USER = $userInfo[0]
        $DB_PASS = $userInfo[1]
        $DB_HOST = $uri.Host
        $DB_PORT = $uri.Port
        $DB_NAME = $uri.AbsolutePath.TrimStart("/")
        
        # Set PGPASSWORD environment variable for psql
        [Environment]::SetEnvironmentVariable("PGPASSWORD", $DB_PASS, "Process")
        
        # Execute SQL script
        psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f create_database.sql
        
        Write-Host "SQL initialization complete." -ForegroundColor Green
    }
    catch {
        Write-Host "Error parsing DATABASE_URL: $_" -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "If you want to run the SQL script directly, use: .\render-db-init.ps1 --sql" -ForegroundColor Yellow
}

Write-Host "Database initialization process complete!" -ForegroundColor Green
