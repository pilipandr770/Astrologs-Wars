"""
Скрипт для ежедневной генерации гороскопов для разных астрологических систем.
Версия с исправленными названиями полей базы данных.
"""
import os
import time
import json
import sys
import re
from datetime import datetime
import logging
from dotenv import load_dotenv
from urllib.parse import urlparse
from sqlalchemy import inspect

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("horoscope_generator.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("HoroscopeGenerator")
logger.info("Starting horoscope generator script")

# Load environment variables
load_dotenv()

# Fix DATABASE_URL if needed - strip any whitespace or newlines
if 'DATABASE_URL' in os.environ:
    original_url = os.environ['DATABASE_URL']
    db_url = original_url.strip()
    os.environ['DATABASE_URL'] = db_url
    
    # Parse the URL for logging (mask password)
    parsed_url = urlparse(db_url)
    masked_url = db_url.replace(parsed_url.password, '****') if parsed_url.password else db_url
    
    # Log the URL cleaning
    if db_url != original_url:
        logger.info(f"Cleaned DATABASE_URL (removed whitespace/newlines)")
    
    # Check if port is missing and add default if needed
    if parsed_url.port is None:
        host_part = f"{parsed_url.hostname}"
        db_part = parsed_url.path
        
        # Reconstruct the URL with the default port
        new_url = f"{parsed_url.scheme}://{parsed_url.username}:{parsed_url.password}@{host_part}:5432{db_part}"
        os.environ['DATABASE_URL'] = new_url
        logger.info(f"Added default port 5432 to DATABASE_URL")
    
    logger.info(f"Using database: {parsed_url.path.strip('/')}")
else:
    logger.error("DATABASE_URL environment variable not found")
    sys.exit(1)

try:
    from openai import OpenAI
    import requests
    from flask import current_app
    import io
    from werkzeug.utils import secure_filename
    import pytz
    import ephem

    from app import create_app, db
    from app.models import BlogBlock
    from app.blog_automation.models import ContentGenerationLog
    from app.utils.file_utils import save_uploaded_file
    from app.utils.text_utils import strip_html_tags
    
    logger.info("All modules imported successfully")
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)

# Initialize Flask app to get database context
try:
    app = create_app()
    app_context = app.app_context()
    app_context.push()
    
    # Inspect database tables to check available columns
    inspector = inspect(db.engine)
    
    # Check BlogBlock columns
    blog_block_columns = [c['name'] for c in inspector.get_columns('blog_block')]
    logger.info(f"BlogBlock columns: {blog_block_columns}")
    
    # Check ContentGenerationLog columns
    content_log_columns = [c['name'] for c in inspector.get_columns('content_generation_log')]
    logger.info(f"ContentGenerationLog columns: {content_log_columns}")
    
    logger.info("Flask application context initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Flask application context: {e}")
    sys.exit(1)

def get_assistants_from_env():
    """
    Получить ID ассистентов для разных астрологических систем из переменных окружения.
    """
    assistants = {}
    
    # Define the mapping of environment variables to assistant names
    env_to_system = {
        "EUROPEAN_ASTROLOGY_ASSISTANT_ID": "european",
        "CHINESE_ASTROLOGY_ASSISTANT_ID": "chinese",
        "INDIAN_ASTROLOGY_ASSISTANT_ID": "indian",
        "LAL_KITAB_ASSISTANT_ID": "lal_kitab",
        "JYOTISH_ASSISTANT_ID": "jyotish",
        "NUMEROLOGY_ASSISTANT_ID": "numerology",
        "TAROT_ASSISTANT_ID": "tarot",
        "PLANETARY_ASTROLOGY_ASSISTANT_ID": "planetary",
        "UKRAINIAN_TRANSLATION_ASSISTANT_ID": "translation_uk"
    }
    
    # Get assistant IDs from environment variables
    for env_var, system_key in env_to_system.items():
        assistant_id = os.environ.get(env_var)
        assistants[system_key] = assistant_id
        logger.info(f"Получен ассистент для {system_key}: переменная {env_var}, ID {assistant_id}")
    
    return assistants

def get_assistant_names():
    """
    Получить словарь с названиями систем на разных языках.
    """
    return {
        "european": {
            "ru": "Европейская астрология",
            "uk": "Європейська астрологія"
        },
        "chinese": {
            "ru": "Китайская астрология",
            "uk": "Китайська астрологія"
        },
        "indian": {
            "ru": "Индийская астрология",
            "uk": "Індійська астрологія"
        },
        "lal_kitab": {
            "ru": "Лал Китаб",
            "uk": "Лал Кітаб"
        },
        "jyotish": {
            "ru": "Джйотиш",
            "uk": "Джйотиш"
        },
        "numerology": {
            "ru": "Нумерология",
            "uk": "Нумерологія"
        },
        "tarot": {
            "ru": "Таро",
            "uk": "Таро"
        },
        "planetary": {
            "ru": "Планетарная астрология",
            "uk": "Планетарна астрологія"
        }
    }

def clean_html_wrapper(content):
    """
    Clean HTML content by removing outer html, body, head, and doctype tags.
    This ensures we store only the content, not the full HTML document.
    """
    if not content:
        return ""
        
    # Remove doctype declaration
    content = re.sub(r'<!DOCTYPE[^>]*>', '', content)
    
    # Remove html, head and body tags
    content = re.sub(r'<html[^>]*>|</html>', '', content)
    content = re.sub(r'<head>.*?</head>', '', content, flags=re.DOTALL)
    content = re.sub(r'<body[^>]*>|</body>', '', content)
    
    # Trim whitespace
    content = content.strip()
    
    return content

def get_blog_block_summary(content, max_length=300):
    """
    Extract a summary from the blog content.
    """
    if not content:
        return ""
        
    # Strip HTML tags for the summary
    plain_text = strip_html_tags(content)
    
    # Get the first few sentences
    summary = plain_text[:max_length]
    
    # Ensure the summary doesn't cut off in the middle of a word
    if len(plain_text) > max_length:
        last_space = summary.rfind(' ')
        if last_space > 0:
            summary = summary[:last_space] + '...'
        else:
            summary += '...'
    
    return summary

def translate_content(content, target_language):
    """
    Translate the content to the specified language using the translation assistant.
    """
    if not content or not target_language:
        return content
        
    # Get the translator assistant ID
    assistant_id = os.environ.get('UKRAINIAN_TRANSLATION_ASSISTANT_ID')
    
    if not assistant_id:
        logger.error("Translation assistant ID not found in environment variables")
        return content  # Return original content if no assistant ID
    
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    
    try:
        thread = client.beta.threads.create()
        
        # Prepare the message for the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Translate the following content to {target_language}. Maintain all HTML formatting and structure in the translation:\n\n{content}"
        )
        
        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        
        # Poll for completion
        for _ in range(30):  # Timeout after 30 attempts (5 minutes)
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break
                
            if run_status.status == 'failed':
                logger.error(f"Translation run failed: {run_status.last_error}")
                return content
                
            time.sleep(10)  # Check every 10 seconds
        
        # Get the response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        translated_content = ""
        
        for msg in messages.data:
            if msg.role == "assistant":
                for content_item in msg.content:
                    if content_item.type == "text":
                        translated_content = content_item.text.value
                        break
        
        # Clean the translated content
        translated_content = clean_html_wrapper(translated_content)
        
        return translated_content
    
    except Exception as e:
        logger.error(f"Error in translation: {str(e)}")
        return content  # Return original content on error

def generate_horoscope_for_system(system_key, assistant_id):
    """
    Generate horoscope for a specific system using the corresponding OpenAI assistant.
    """
    if not assistant_id:
        logger.warning(f"No assistant ID provided for {system_key}, skipping generation")
        return None
        
    assistant_names = get_assistant_names()
    system_name_ru = assistant_names.get(system_key, {}).get('ru', system_key)
    
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    
    try:
        # Create a new thread for the conversation
        thread = client.beta.threads.create()
        
        # Get today's date for the horoscope
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Prepare the message for the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user", 
            content=f"Создай ежедневный гороскоп в системе {system_name_ru} на {today}. Включи полезные советы для каждого знака зодиака."
        )
        
        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        
        # Poll for completion
        for _ in range(30):  # Timeout after 30 attempts (5 minutes)
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break
                
            if run_status.status == 'failed':
                logger.error(f"{system_key} horoscope generation failed: {run_status.last_error}")
                return None
                
            time.sleep(10)  # Check every 10 seconds
        
        # Get the response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        horoscope_content = ""
        
        for msg in messages.data:
            if msg.role == "assistant":
                for content_item in msg.content:
                    if content_item.type == "text":
                        horoscope_content = content_item.text.value
                        break
        
        horoscope_content = clean_html_wrapper(horoscope_content)
        return horoscope_content
        
    except Exception as e:
        logger.error(f"Error generating {system_key} horoscope: {str(e)}")
        return None

def create_horoscope_block(system_key, content):
    """
    Create a blog block for the horoscope content with dynamic field handling.
    """
    if not content:
        logger.warning(f"No content provided for {system_key} horoscope block")
        return None
        
    try:
        assistant_names = get_assistant_names()
        system_name_ru = assistant_names.get(system_key, {}).get('ru', system_key)
        system_name_uk = assistant_names.get(system_key, {}).get('uk', system_key)
        
        # Prepare base data with correct field names
        # Using created_at instead of date_created
        today = datetime.now().date()
        
        # Create a dictionary for BlogBlock initialization
        blog_data = {
            'title_ru': f"{system_name_ru} на {today.strftime('%d.%m.%Y')}",
            'content_ru': content,
            'summary_ru': get_blog_block_summary(content),
            'created_at': datetime.now(),  # Use created_at instead of date_created
            'block_type': "horoscope",
            'subtype': system_key,
            'is_published': True,
            'is_featured': True,
        }
        
        # Check if database has Ukrainian language support columns
        # Only add these fields if they exist in the database
        has_uk_support = all(col in blog_block_columns for col in ['title_uk', 'content_uk', 'summary_uk'])
        
        if has_uk_support:
            # Translate content to Ukrainian only if the database supports it
            uk_content = translate_content(content, "Ukrainian")
            
            blog_data.update({
                'title_uk': f"{system_name_uk} на {today.strftime('%d.%m.%Y')}",
                'content_uk': uk_content,
                'summary_uk': get_blog_block_summary(uk_content) if uk_content else ""
            })
            logger.info(f"Added Ukrainian fields for {system_key} horoscope")
        else:
            logger.warning(f"Database doesn't support Ukrainian fields for {system_key} horoscope")
        
        # Create the blog block with the appropriate fields
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
    Log generation activity to the database with dynamic field handling
    """
    try:
        # Create a dictionary for ContentGenerationLog initialization
        # Using created_at instead of timestamp
        log_data = {
            'status': "success" if success else "failed",
            'message': message,
            'created_at': datetime.now()  # Use created_at instead of timestamp
        }
        
        # Add system field only if it exists in the database
        if 'system' in content_log_columns:
            log_data['system'] = system
        
        log = ContentGenerationLog(**log_data)
        db.session.add(log)
        db.session.commit()
        logger.info(f"Logged generation activity for {system}: {'success' if success else 'failed'}")
    except Exception as e:
        logger.error(f"Failed to log generation activity: {e}")
        db.session.rollback()

def notify_telegram(message):
    """
    Send notification to Telegram channel.
    """
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    channel = os.environ.get('TELEGRAM_CHANNEL_NAME')
    
    if not bot_token or not channel:
        logger.info("Telegram notification skipped - bot token or channel not configured")
        return
        
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": channel,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        logger.info(f"Telegram notification sent: {message}")
    except Exception as e:
        logger.error(f"Failed to send Telegram notification: {e}")

def main():
    """
    Основная функция для генерации и сохранения гороскопов.
    """
    logger.info("Starting daily horoscope generation")
    
    # Get assistant IDs from environment variables
    assistants = get_assistants_from_env()
    
    # Track statistics
    successful_systems = []
    failed_systems = []
    
    # Generate horoscopes for each system
    for system_key, assistant_id in assistants.items():
        if not assistant_id or system_key == "translation_uk":  # Skip the translator
            if system_key != "translation_uk":
                logger.warning(f"Skipping {system_key} - no assistant ID configured")
                failed_systems.append(system_key)
            continue
            
        try:
            logger.info(f"Generating {system_key} horoscope")
            horoscope_content = generate_horoscope_for_system(system_key, assistant_id)
            
            if horoscope_content:
                blog_block = create_horoscope_block(system_key, horoscope_content)
                if blog_block:
                    successful_systems.append(system_key)
                    log_generation_activity(system_key, True)
                else:
                    failed_systems.append(system_key)
                    log_generation_activity(system_key, False, "Failed to create blog block")
            else:
                failed_systems.append(system_key)
                log_generation_activity(system_key, False, "No content generated")
                
        except Exception as e:
            logger.error(f"Error processing {system_key} horoscope: {str(e)}")
            failed_systems.append(system_key)
            log_generation_activity(system_key, False, str(e))
    
    # Send summary notification
    summary = f"📊 Daily Horoscope Generation Report:\n"
    summary += f"✅ Success: {len(successful_systems)} systems\n"
    if successful_systems:
        summary += "- " + ", ".join(successful_systems) + "\n"
    
    summary += f"❌ Failed: {len(failed_systems)} systems\n"
    if failed_systems:
        summary += "- " + ", ".join(failed_systems)
        
    logger.info(summary)
    notify_telegram(summary)
    
    # Clean up
    db.session.close()

if __name__ == "__main__":
    try:
        main()
        logger.info("Daily horoscope generation completed")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Uncaught exception in main: {str(e)}")
        sys.exit(1)
    finally:
        # Make sure to pop the app context
        try:
            app_context.pop()
        except Exception:
            pass
