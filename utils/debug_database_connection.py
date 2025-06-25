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
# Check for and strip any trailing whitespace or newlines
db_url = db_url.strip()
print("Stripped DATABASE_URL:", repr(db_url))

# Parse the DATABASE_URL
try:
    result = urlparse(db_url)
    username = result.username
    password = result.password
    hostname = result.hostname
    port = result.port
    database = result.path.strip('/')
    
    print("\nParsed components:")
    print(f"Username: {username}")
    print(f"Password: {'*' * (len(password) if password else 0)}")
    print(f"Hostname: {hostname}")
    print(f"Port: {port}")
    print(f"Database: {repr(database)}")
    
except Exception as e:
    print(f"Error parsing DATABASE_URL: {str(e)}")
    sys.exit(1)

# Try connecting to the database
print("\nAttempting connection to database...")
try:
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    
    # Check connection by running a simple query
    cursor.execute("SELECT current_database();")
    current_db = cursor.fetchone()[0]
    print(f"Successfully connected to database: {current_db}")
    
    # Check if the database exists
    cursor.execute("SELECT datname FROM pg_database WHERE datname = %s;", (database,))
    if cursor.fetchone():
        print(f"Database '{database}' exists")
    else:
        print(f"Database '{database}' does not exist")
    
    # List all databases
    print("\nList of all databases on the server:")
    cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
    databases = cursor.fetchall()
    for db in databases:
        print(f"- {db[0]}")
    
    conn.close()
except Exception as e:
    print(f"Error connecting to database: {str(e)}")
    
print("\nFixing recommendations:")
print("1. Make sure the database name in your connection string matches exactly with an existing database")
print("2. Check for any trailing spaces or newlines in your DATABASE_URL")
print("3. Confirm the port is correct (usually 5432 for PostgreSQL)")
print("4. Verify credentials (username/password) are correct")
print("5. Ensure the database server allows connections from Render IP addresses")
