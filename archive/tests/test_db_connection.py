#!/usr/bin/env python3
# test_db_connection.py - Test PostgreSQL database connection

from dotenv import load_dotenv
load_dotenv()

import os
import sys
import time

print("Testing database connection...")
print(f"DATABASE_URL: {os.environ.get('DATABASE_URL', 'Not set')}")

if not os.environ.get("DATABASE_URL"):
    print("ERROR: DATABASE_URL environment variable is not set.")
    sys.exit(1)

if not os.environ.get("DATABASE_URL").startswith("postgresql://"):
    print("ERROR: This script is intended to test PostgreSQL connections.")
    print("Your DATABASE_URL does not appear to be a PostgreSQL URL.")
    sys.exit(1)

try:
    print("Attempting to connect to the database...")
    
    # Import SQLAlchemy and create a test connection
    from sqlalchemy import create_engine, text
    
    # Create engine with a timeout
    engine = create_engine(os.environ.get("DATABASE_URL"), connect_args={"connect_timeout": 10})
    
    # Try to connect and run a simple query
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.scalar()
        print(f"Success! Connected to PostgreSQL.")
        print(f"Database version: {version}")
        
        # Check if our tables exist
        print("\nChecking for application tables...")
        tables = [
            "user", "block", "payment_method", "payment", "settings", 
            "category", "product", "product_image", "cart", "cart_item",
            "order", "order_item", "blog_block", "blog_topic",
            "autoposting_schedule", "content_generation_log"
        ]
        
        for table in tables:
            try:
                result = connection.execute(text(f"SELECT COUNT(*) FROM \"{table}\";"))
                count = result.scalar()
                print(f"Table '{table}' exists with {count} rows")
            except Exception as e:
                print(f"Table '{table}' not found or error: {str(e)}")
    
    print("\nDatabase connection test completed successfully!")
    
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Please run: pip install sqlalchemy")
    sys.exit(1)
    
except Exception as e:
    print(f"ERROR: Failed to connect to the database: {str(e)}")
    print("\nPossible issues:")
    print("1. Database server is not running")
    print("2. Connection string is incorrect")
    print("3. Network/firewall is blocking the connection")
    print("4. Database user doesn't have proper permissions")
    
    if "password authentication failed" in str(e).lower():
        print("\nAuthentication failed. Check your username and password.")
    elif "could not translate host" in str(e).lower():
        print("\nHost name could not be resolved. Check the server address.")
    elif "connection refused" in str(e).lower():
        print("\nConnection refused. The server may be down or the port is blocked.")
    elif "timeout expired" in str(e).lower():
        print("\nConnection timeout. The server may be unreachable or behind a firewall.")
    
    sys.exit(1)
