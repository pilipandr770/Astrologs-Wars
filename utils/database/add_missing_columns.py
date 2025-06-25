"""
Script to add missing columns to database tables
"""
import os
import sys
import logging
from dotenv import load_dotenv
from sqlalchemy import inspect, text

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DBColumnFixer")

# Load environment variables
load_dotenv()

# Fix DATABASE_URL if needed
if 'DATABASE_URL' in os.environ:
    original_url = os.environ['DATABASE_URL']
    db_url = original_url.strip()
    os.environ['DATABASE_URL'] = db_url
    logger.info(f"Using cleaned DATABASE_URL")

try:
    from app import create_app, db
    logger.info("All modules imported successfully")
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)

def execute_sql(sql):
    """Execute SQL statement safely"""
    try:
        with db.engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()
        return True
    except Exception as e:
        logger.error(f"SQL error: {e}")
        return False

def check_column_exists(table, column):
    """Check if a column exists in a table"""
    try:
        inspector = inspect(db.engine)
        columns = [c['name'] for c in inspector.get_columns(table)]
        return column in columns
    except Exception as e:
        logger.error(f"Error checking column existence: {e}")
        return False

def add_column_if_missing(table, column, data_type):
    """Add a column to a table if it doesn't exist"""
    if not check_column_exists(table, column):
        logger.info(f"Adding missing column '{column}' to table '{table}'")
        sql = f"ALTER TABLE {table} ADD COLUMN {column} {data_type};"
        if execute_sql(sql):
            logger.info(f"Successfully added column '{column}' to '{table}'")
            return True
        else:
            logger.error(f"Failed to add column '{column}' to '{table}'")
            return False
    else:
        logger.info(f"Column '{column}' already exists in '{table}'")
        return True

def main():
    """Main function to add missing columns"""
    try:
        # Initialize app and push context
        app = create_app()
        ctx = app.app_context()
        ctx.push()
        
        # Add missing columns to blog_block table
        add_column_if_missing('blog_block', 'title_uk', 'VARCHAR(255)')
        add_column_if_missing('blog_block', 'content_uk', 'TEXT')
        add_column_if_missing('blog_block', 'summary_uk', 'TEXT')
        
        # Add missing columns to content_generation_log table
        add_column_if_missing('content_generation_log', 'system', 'VARCHAR(255)')
        
        # Display table structure after updates
        inspector = inspect(db.engine)
        for table_name in ['blog_block', 'content_generation_log']:
            columns = inspector.get_columns(table_name)
            logger.info(f"Table '{table_name}' columns after update:")
            for col in columns:
                logger.info(f"  - {col['name']} ({col['type']})")
        
        # Clean up
        ctx.pop()
        logger.info("Database update completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
