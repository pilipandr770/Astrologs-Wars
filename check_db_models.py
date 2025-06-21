"""
Script to check and verify database models in the application
"""
import os
import sys
import logging
from dotenv import load_dotenv
from sqlalchemy import inspect, text

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ModelChecker")

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
    from app.models import BlogBlock
    from app.blog_automation.models import ContentGenerationLog
    
    logger.info("All modules imported successfully")
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)

def check_table_columns(table_name):
    """Check the columns for a specific table"""
    try:
        # Create an inspector
        inspector = inspect(db.engine)
        
        if table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            logger.info(f"Table '{table_name}' exists with columns:")
            for column in columns:
                logger.info(f"  - {column['name']} ({column['type']})")
            return columns
        else:
            logger.error(f"Table '{table_name}' does not exist in the database")
            return None
    except Exception as e:
        logger.error(f"Error checking table columns: {e}")
        return None

def print_model_attributes(model_class):
    """Print the attributes of a model class"""
    logger.info(f"Model class {model_class.__name__} attributes:")
    for key in model_class.__mapper__.attrs.keys():
        logger.info(f"  - {key}")
        
def execute_raw_sql(sql):
    """Execute raw SQL query"""
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text(sql))
            if sql.strip().lower().startswith('select'):
                rows = result.fetchall()
                return rows
            return None
    except Exception as e:
        logger.error(f"Error executing SQL: {e}")
        return None

def add_column_if_missing(table_name, column_name, column_type):
    """Add a column to a table if it doesn't exist"""
    try:
        # Check if the column exists
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        
        if column_name not in columns:
            logger.info(f"Adding missing column '{column_name}' to table '{table_name}'")
            sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};"
            execute_raw_sql(sql)
            logger.info(f"Column '{column_name}' added successfully")
            return True
        else:
            logger.info(f"Column '{column_name}' already exists in table '{table_name}'")
            return False
    except Exception as e:
        logger.error(f"Error adding column: {e}")
        return False

def main():
    """Main function to check and update the database models"""
    try:
        # Initialize app and push context
        app = create_app()
        ctx = app.app_context()
        ctx.push()
        
        logger.info("Checking database tables and models")
        
        # Check BlogBlock table
        blog_block_columns = check_table_columns('blog_block')
        print_model_attributes(BlogBlock)
        
        # Check ContentGenerationLog table
        content_log_columns = check_table_columns('content_generation_log')
        print_model_attributes(ContentGenerationLog)
        
        # Add missing columns if needed
        add_column_if_missing('blog_block', 'title_uk', 'VARCHAR(255)')
        add_column_if_missing('blog_block', 'content_uk', 'TEXT')
        add_column_if_missing('blog_block', 'summary_uk', 'TEXT')
        add_column_if_missing('content_generation_log', 'system', 'VARCHAR(255)')
        
        # Verify tables again after adding columns
        logger.info("Verifying tables after updates:")
        check_table_columns('blog_block')
        check_table_columns('content_generation_log')
        
        # Clean up
        ctx.pop()
        logger.info("Database check completed")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
