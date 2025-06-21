"""
Script to check the actual fields of the BlogBlock and ContentGenerationLog models.
"""
import os
import sys
import logging
from dotenv import load_dotenv
from sqlalchemy import inspect, text

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ModelFieldsChecker")

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

def print_model_attributes(model_class):
    """Print the attributes of a model class"""
    logger.info(f"Model class {model_class.__name__} attributes:")
    for key in model_class.__mapper__.attrs.keys():
        logger.info(f"  - {key}")

def get_model_init_params(model_class):
    """Get the parameters accepted by the model's __init__ method"""
    from inspect import signature
    
    try:
        sig = signature(model_class.__init__)
        params = list(sig.parameters.keys())
        # Remove 'self' from the list
        if 'self' in params:
            params.remove('self')
        
        logger.info(f"{model_class.__name__} __init__ accepts parameters: {params}")
        return params
    except Exception as e:
        logger.error(f"Error inspecting __init__ of {model_class.__name__}: {e}")
        return []

def check_table_columns(table_name):
    """Check the columns for a specific table"""
    try:
        # Create an inspector
        inspector = inspect(db.engine)
        
        if table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            logger.info(f"Table '{table_name}' has the following columns:")
            for column in columns:
                logger.info(f"  - {column['name']} ({column['type']})")
            return columns
        else:
            logger.error(f"Table '{table_name}' does not exist in the database")
            return None
    except Exception as e:
        logger.error(f"Error checking table columns: {e}")
        return None

def check_instance_creation(model_class):
    """Try to create an instance with different parameters to see what works"""
    logger.info(f"Testing instance creation for {model_class.__name__}")
    
    # Try with basic attributes
    try:
        if model_class.__name__ == 'BlogBlock':
            instance = model_class(
                title='Test',
                content='Test content',
                summary='Test summary',
                is_active=True
            )
            logger.info("Successfully created BlogBlock with basic attributes")
        elif model_class.__name__ == 'ContentGenerationLog':
            instance = model_class(
                status='success',
                message='Test message'
            )
            logger.info("Successfully created ContentGenerationLog with basic attributes")
    except Exception as e:
        logger.error(f"Error creating instance: {e}")

def main():
    """Main function to check and analyze the model fields"""
    try:
        # Initialize app and push context
        app = create_app()
        ctx = app.app_context()
        ctx.push()
        
        logger.info("Checking model fields and database tables")
        
        # Check BlogBlock model
        logger.info("\n=== BlogBlock Model ===")
        print_model_attributes(BlogBlock)
        get_model_init_params(BlogBlock)
        check_table_columns('blog_block')
        check_instance_creation(BlogBlock)
        
        # Check ContentGenerationLog model
        logger.info("\n=== ContentGenerationLog Model ===")
        print_model_attributes(ContentGenerationLog)
        get_model_init_params(ContentGenerationLog)
        check_table_columns('content_generation_log')
        check_instance_creation(ContentGenerationLog)
        
        # Clean up
        ctx.pop()
        logger.info("Model fields check completed")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
