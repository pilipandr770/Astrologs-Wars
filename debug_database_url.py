#!/usr/bin/env python3
"""
Debug script to check DATABASE_URL environment variable for hidden characters
"""

import os
import sys

# Get the DATABASE_URL
db_url = os.environ.get("DATABASE_URL", "Not set")

print("=== DATABASE_URL DEBUG ===")
print(f"Raw value: {repr(db_url)}")
print(f"Length: {len(db_url)}")
print(f"Ends with newline: {db_url.endswith('\\n')}")
print(f"Contains newline: {'\\n' in db_url}")

if db_url != "Not set":
    # Extract database name from URL
    if "/" in db_url:
        db_name = db_url.split("/")[-1]
        print(f"Database name: {repr(db_name)}")
        print(f"DB name length: {len(db_name)}")
        print(f"DB name ends with newline: {db_name.endswith('\\n')}")
        
    # Show byte representation
    print(f"Bytes: {db_url.encode('utf-8')}")

print("=== END DEBUG ===")
