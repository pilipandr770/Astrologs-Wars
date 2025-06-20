import os
import sys
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Get DATABASE_URL from environment variables
db_url = os.getenv('DATABASE_URL')

# Fix for Windows line ending issues - remove all line breaks and whitespace
if db_url:
    # Show if there are any special characters
    print("Original DATABASE_URL with repr:", repr(db_url))
    
    # Replace any \r\n, \r, \n with empty string and strip whitespace
    db_url = re.sub(r'[\r\n\t]+', '', db_url).strip()
    print("Cleaned DATABASE_URL:", repr(db_url))
    
    # Update environment variable
    os.environ['DATABASE_URL'] = db_url
    
    # Write the cleaned URL back to .env file
    env_content = ""
    with open('.env', 'r') as f:
        env_content = f.read()
    
    # Replace the DATABASE_URL line in the .env file
    pattern = r'DATABASE_URL=.*'
    replacement = f'DATABASE_URL={db_url}'
    env_content = re.sub(pattern, replacement, env_content)
    
    with open('.env.clean', 'w') as f:
        f.write(env_content)
    
    print("Created clean .env file at .env.clean")
    
    # Test connection with cleaned URL
    try:
        print("\nTesting database connection with cleaned URL...")
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        cursor.execute("SELECT current_database();")
        current_db = cursor.fetchone()[0]
        print(f"Successfully connected to database: {current_db}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
else:
    print("DATABASE_URL environment variable not found")
