#!/usr/bin/env python3
"""
Test script to verify database connection with the corrected connection string.
"""

import os
import psycopg2
from sqlalchemy import create_engine, text

# Test connection string with explicit port
connection_string = "postgresql://ittoken_db_user:Xm98VVSZv7cMJkopkdWRkgvZzC7Aly42@dpg-d0visga4d50c73ekmu4g-a.oregon-postgres.render.com:5432/astro_blog_db"

print("Testing database connection...")
print(f"Connection string: {connection_string[:50]}...")

try:
    # Test with SQLAlchemy (what our app uses)
    engine = create_engine(connection_string)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT current_database(), version()"))
        row = result.fetchone()
        print(f"✅ SQLAlchemy connection successful!")
        print(f"Current database: {row[0]}")
        print(f"PostgreSQL version: {row[1][:50]}...")
        
except Exception as e:
    print(f"❌ SQLAlchemy connection failed: {e}")

try:
    # Test with psycopg2 directly
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT current_database(), version()")
    row = cursor.fetchone()
    print(f"✅ psycopg2 connection successful!")
    print(f"Current database: {row[0]}")
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ psycopg2 connection failed: {e}")

print("\nDatabase connection test completed.")
