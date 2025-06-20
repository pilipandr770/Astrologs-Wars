import os
import sys
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get DATABASE_URL from environment variables
db_url = os.getenv('DATABASE_URL')

if not db_url:
    print("Error: DATABASE_URL environment variable not found")
    sys.exit(1)

print("Original DATABASE_URL:", repr(db_url))
db_url = db_url.strip()
print("Stripped DATABASE_URL:", repr(db_url))

# Parse the DATABASE_URL to extract database name and connection info
result = urlparse(db_url)
username = result.username
password = result.password
hostname = result.hostname
port = result.port if result.port else 5432
database = result.path.strip('/')

print(f"\nDatabase name: {repr(database)}")

# Form a connection URL to the PostgreSQL server without specifying a database
server_url = f"postgresql://{username}:{password}@{hostname}:{port}/postgres"

try:
    # Connect to the default postgres database first
    conn = psycopg2.connect(server_url)
    conn.autocommit = True  # This is required for creating databases
    cursor = conn.cursor()
    
    # Check if our target database exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (database,))
    exists = cursor.fetchone()
    
    if not exists:
        print(f"Database '{database}' does not exist. Creating now...")
        # SQL to create a new database
        sql = f"CREATE DATABASE {database};"
        cursor.execute(sql)
        print(f"Database '{database}' created successfully!")
    else:
        print(f"Database '{database}' already exists!")
    
    # Close connection to postgres database
    cursor.close()
    conn.close()
    
    # Now try connecting to the target database to verify
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    cursor.execute("SELECT current_database();")
    current_db = cursor.fetchone()[0]
    print(f"Successfully connected to database: {current_db}")
    cursor.close()
    conn.close()
    
    print("\nDatabase connection successful!")
    
except Exception as e:
    print(f"Error: {str(e)}")
    print("\nPossible solutions:")
    print("1. Check if your database service is running")
    print("2. Verify that the database credentials are correct")
    print("3. Ensure that your IP is allowed to access the database")
    print("4. Check if you have sufficient privileges to create databases")
    sys.exit(1)
