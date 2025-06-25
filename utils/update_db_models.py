"""
Script to update database models to match our application requirements
"""
import os
import sys
import logging
from dotenv import load_dotenv
from sqlalchemy import inspect, text

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ModelUpdater")

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

def check_column_exists(table_name, column_name):
    """Check if a column exists in a table"""
    try:
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        return column_name in columns
    except Exception as e:
        logger.error(f"Error checking if column exists: {e}")
        return False

def add_column(table_name, column_name, column_type):
    """Add a column to a table"""
    try:
        if not check_column_exists(table_name, column_name):
            sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};"
            with db.engine.connect() as connection:
                connection.execute(text(sql))
                connection.commit()
            logger.info(f"Added column '{column_name}' to table '{table_name}'")
            return True
        else:
            logger.info(f"Column '{column_name}' already exists in table '{table_name}'")
            return False
    except Exception as e:
        logger.error(f"Error adding column: {e}")
        return False

def check_and_update_models():
    """Check and update database models to match our application requirements"""
    try:
        # Update BlogBlock model
        needed_blog_columns = {
            'title_uk': 'VARCHAR(255)',
            'content_uk': 'TEXT',
            'summary_uk': 'TEXT'
        }
        
        for column_name, column_type in needed_blog_columns.items():
            add_column('blog_block', column_name, column_type)
        
        # Update ContentGenerationLog model
        add_column('content_generation_log', 'system', 'VARCHAR(255)')
        
        logger.info("Database models updated successfully")
        return True
    except Exception as e:
        logger.error(f"Error updating models: {e}")
        return False

def update_generator_script():
    """Update the horoscope generator script to check for required fields"""
    modified_script = """
'''
Модифицированный скрипт для создания блога, который проверяет наличие полей перед использованием
'''

def create_horoscope_block(system_key, content):
    """
    Create a blog block for the horoscope content with field checking.
    """
    if not content:
        logger.warning(f"No content provided for {system_key} horoscope block")
        return None
        
    try:
        assistant_names = get_assistant_names()
        system_name_ru = assistant_names.get(system_key, {}).get('ru', system_key)
        system_name_uk = assistant_names.get(system_key, {}).get('uk', system_key)
        
        # Translate content to Ukrainian
        uk_content = translate_content(content, "Ukrainian")
        
        # Prepare dates and summaries
        today = datetime.now().date()
        timestamp = int(datetime.now().timestamp())
        
        # Get clean summaries for all content
        ru_summary = get_blog_block_summary(content)
        uk_summary = get_blog_block_summary(uk_content) if uk_content else ""
        
        # Create a new blog block with field checking
        blog_data = {
            'title_ru': f"{system_name_ru} на {today.strftime('%d.%m.%Y')}",
            'content_ru': content,
            'summary_ru': ru_summary,
            'date_created': today,
            'timestamp': timestamp,
            'block_type': "horoscope",
            'subtype': system_key,
            'is_published': True,
            'is_featured': True
        }
        
        # Check if Ukrainian fields are supported by the model
        blog_block_columns = [c.key for c in BlogBlock.__table__.columns]
        
        if 'title_uk' in blog_block_columns:
            blog_data['title_uk'] = f"{system_name_uk} на {today.strftime('%d.%m.%Y')}"
            
        if 'content_uk' in blog_block_columns:
            blog_data['content_uk'] = uk_content
            
        if 'summary_uk' in blog_block_columns:
            blog_data['summary_uk'] = uk_summary
        
        # Create the blog block with only the supported fields
        blog_block = BlogBlock(**blog_data)
        
        db.session.add(blog_block)
        db.session.commit()
        
        logger.info(f"Created {system_key} horoscope block ID: {blog_block.id}")
        return blog_block
        
    except Exception as e:
        logger.error(f"Error creating {system_key} horoscope block: {str(e)}")
        db.session.rollback()
        return None

def log_generation_activity(system, success, message=""):
    """
    Log generation activity to the database with field checking
    """
    try:
        # Check if the ContentGenerationLog model has a 'system' field
        log_data = {
            'status': "success" if success else "failed",
            'message': message,
            'timestamp': datetime.now()
        }
        
        # Check if ContentGenerationLog has a 'system' field
        log_columns = [c.key for c in ContentGenerationLog.__table__.columns]
        if 'system' in log_columns:
            log_data['system'] = system
        
        log = ContentGenerationLog(**log_data)
        db.session.add(log)
        db.session.commit()
        logger.info(f"Logged generation activity for {system}: {'success' if success else 'failed'}")
    except Exception as e:
        logger.error(f"Failed to log generation activity: {e}")
        db.session.rollback()
"""

    return modified_script

def main():
    """Main function to update database models and scripts"""
    try:
        # Initialize app and push context
        app = create_app()
        ctx = app.app_context()
        ctx.push()
        
        logger.info("Starting database model update")
        
        # Check and update models
        check_and_update_models()
        
        # Generate modified script
        script_content = update_generator_script()
        with open('fix_horoscope_generator.py', 'w') as f:
            f.write(script_content)
        
        logger.info("Modified generator script created at fix_horoscope_generator.py")
        
        # Clean up
        ctx.pop()
        logger.info("Database model update completed")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
