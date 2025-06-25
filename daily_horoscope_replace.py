"""
Улучшенный скрипт для ежедневной генерации гороскопов с интегрированной генерацией изображений.
Заменяет старые гороскопы вместо добавления новых и очищает неиспользуемые изображения.

Последнее обновление: 25.06.2025
- Добавлен автоматический перевод гороскопов на английский, немецкий и русский языки
- Добавлена генерация изображений с помощью DALL-E 3
- Созданы уникальные промты для каждой астрологической системы
- Реализован механизм автоматического переключения на локальную генерацию, если DALL-E недоступен
- Добавлены уникальные фоны для каждой астрологической системы
- Добавлены кольца планет и спутники для разных систем
- Добавлены названия астрологических систем в изображения
"""
import os
import time
import json
import sys
import re
import logging
import glob
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from urllib.parse import urlparse
from sqlalchemy import inspect, text, delete
from PIL import Image, ImageDraw, ImageFont
import random
import uuid
import io
from openai import OpenAI
from translator import HoroscopeTranslator

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
logger.info("Starting horoscope generator script with image creation and cleanup")

# Load environment variables
load_dotenv()

# Log OpenAI configuration
if 'OPENAI_API_KEY' in os.environ:
    logger.info("OPENAI_API_KEY is configured")
else:
    logger.warning("OPENAI_API_KEY is not configured - features will be limited")

# Check for astrology assistant IDs
assistant_ids = {
    'EUROPEAN_ASTROLOGY_ASSISTANT_ID': os.environ.get('EUROPEAN_ASTROLOGY_ASSISTANT_ID'),
    'CHINESE_ASTROLOGY_ASSISTANT_ID': os.environ.get('CHINESE_ASTROLOGY_ASSISTANT_ID'),
    'INDIAN_ASTROLOGY_ASSISTANT_ID': os.environ.get('INDIAN_ASTROLOGY_ASSISTANT_ID'),
    'LAL_KITAB_ASSISTANT_ID': os.environ.get('LAL_KITAB_ASSISTANT_ID'),
    'JYOTISH_ASSISTANT_ID': os.environ.get('JYOTISH_ASSISTANT_ID'),
    'NUMEROLOGY_ASSISTANT_ID': os.environ.get('NUMEROLOGY_ASSISTANT_ID'),
    'TAROT_ASSISTANT_ID': os.environ.get('TAROT_ASSISTANT_ID'),
    'PLANETARY_ASTROLOGY_ASSISTANT_ID': os.environ.get('PLANETARY_ASTROLOGY_ASSISTANT_ID')
}

# Log which assistant IDs are configured
configured_assistants = [name for name, id_value in assistant_ids.items() if id_value]
if configured_assistants:
    logger.info(f"Found {len(configured_assistants)} configured astrology assistants: {', '.join(configured_assistants)}")
else:
    logger.warning("No astrology assistant IDs are configured - will use fallback content")

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

# Import app only after setting environment variables
from app import create_app, db
from app.models import BlogBlock

app = create_app()

def cleanup_old_horoscope_images(current_date, keep_positions=None):
    """
    Clean up old horoscope images except the ones we're currently using
    
    Args:
        current_date: Current date for filename generation
        keep_positions: List of position numbers to keep
    """
    if keep_positions is None:
        keep_positions = list(range(1, 9))  # Default: keep all 8 positions
        
    # Ensure the keep_positions are converted to strings for comparison
    keep_positions = [str(pos) for pos in keep_positions]
    
    # Create the date string for current images (we always keep these)
    current_date_str = current_date.strftime("%Y%m%d")
    
    # Get the uploads directory
    upload_dir = os.path.join(app.root_path, 'static', 'uploads', 'blog')
    if not os.path.exists(upload_dir):
        logger.warning(f"Blog uploads directory doesn't exist: {upload_dir}")
        return []
        
    # Get list of all astro image files
    horoscope_image_pattern = os.path.join(upload_dir, "astro_*.png")
    image_files = glob.glob(horoscope_image_pattern)
    
    # Keep track of what we're deleting and keeping
    deleted_files = []
    
    # Process each file
    for image_path in image_files:
        filename = os.path.basename(image_path)
        
        # Skip current date files - we always keep today's files
        if current_date_str in filename:
            continue
            
        # Parse the filename (format: astro_1_20250621.png)
        parts = filename.split('_')
        if len(parts) == 3:
            position = parts[1]
            date_part = parts[2].split('.')[0]
            
            # Only delete if it's not in our keep list
            if position not in keep_positions:
                try:
                    os.remove(image_path)
                    deleted_files.append(filename)
                    logger.info(f"Deleted old image: {filename}")
                except Exception as e:
                    logger.error(f"Failed to delete {filename}: {str(e)}")
    
    logger.info(f"Cleaned up {len(deleted_files)} old horoscope images")
    return deleted_files

def generate_dalle_image(system_name, title, current_date, upload_dir, filename, width=1024, height=1024):
    """
    Generate an image using DALL-E 3 for the specific astrology system
    
    Args:
        system_name: Name of the astrology system
        title: Title of the horoscope
        current_date: Current date for context
        upload_dir: Directory to save the image
        filename: Filename to save as
        width/height: Image dimensions
        
    Returns:
        Success status and filename if successful
    """
    try:
        # Initialize OpenAI client
        client = OpenAI()
        
        # Date info for the prompt
        date_str = current_date.strftime("%d %B %Y")
        
        # System-specific prompts
        system_prompts = {
            "European Astrology": f"Create a mystical, cosmic image representing Western/European astrology for {date_str}. "
                                 f"Include zodiac symbols subtly arranged in a celestial pattern with stars and planets. "
                                 f"Use deep blues and purples with gold accents. Make it look professional and elegant "
                                 f"for a horoscope website. No text overlay.",
                                 
            "Chinese Astrology": f"Create an artistic representation of Chinese astrology for {date_str}. "
                               f"Include subtle elements of the Chinese zodiac animals, yin-yang symbols, and "
                               f"traditional Chinese cosmic imagery. Use rich reds, golds and deep purples. "
                               f"Style should be elegant and mystical. No text overlay.",
                               
            "Indian Astrology": f"Create a beautiful Vedic/Indian astrology image for {date_str}. "
                              f"Include subtle imagery of Vedic astrology symbols, cosmic elements, and "
                              f"traditional Indian spiritual imagery. Use warm oranges, deep blues and gold accents. "
                              f"Make it look professional for a horoscope website. No text overlay.",
                              
            "Lal Kitab": f"Create a mystical image representing Lal Kitab astrology for {date_str}. "
                       f"Include subtle elements of planets, karma symbols, and remedies in a "
                       f"cosmic arrangement. Use deep reds, greens, and gold colors. "
                       f"Style should be elegant and mystical. No text overlay.",
                       
            "Jyotish": f"Create an artistic cosmic image representing Jyotish astrology for {date_str}. "
                     f"Include subtle planetary symbols, stars, and traditional Vedic spiritual elements "
                     f"arranged in a celestial pattern. Use deep purples, blues and gold accents. "
                     f"Style should be professional and mystical. No text overlay.",
                     
            "Numerology": f"Create a mesmerizing image representing Numerology for {date_str}. "
                        f"Include subtle numerical symbols, sacred geometry patterns, and cosmic elements. "
                        f"Use blues, golds, and white colors. Style should be mathematical yet mystical. "
                        f"No text overlay.",
                        
            "Tarot": f"Create a mystical image representing Tarot divination for {date_str}. "
                   f"Include subtle imagery of cosmic elements, mystical symbols, and etheric energy. "
                   f"No specific tarot cards should be identifiable. Use rich colors like deep blues, "
                   f"purples, and gold accents. Style should be elegant and mysterious. No text overlay.",
                   
            "Planetary Astrology": f"Create a cosmic image representing Planetary astrology for {date_str}. "
                                f"Include subtle imagery of planets, orbital paths, and celestial bodies "
                                f"in a mystical arrangement. Use deep space blues and cosmic colors. "
                                f"Style should be scientific yet mystical. No text overlay."
        }
        
        # Get the specific prompt for this system or use a generic one
        prompt = system_prompts.get(system_name, 
            f"Create a professional, cosmic image representing {system_name} for horoscope dated {date_str}. "
            f"Use mystical elements, stars, planets and cosmic imagery. No text overlay.")
            
        logger.info(f"Generating DALL-E image for {system_name} with prompt: {prompt[:100]}...")
        
        # Call DALL-E API
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=f"{width}x{height}",
            quality="standard",
            n=1
        )
        
        # Get image URL
        image_url = response.data[0].url
        logger.info(f"Successfully generated DALL-E image for {system_name}")
        
        # Download the image
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # Save the image
            full_path = os.path.join(upload_dir, filename)
            with open(full_path, 'wb') as f:
                f.write(image_response.content)
                
            logger.info(f"Saved DALL-E image for {system_name} as {filename}")
            return True, filename
        else:
            logger.error(f"Failed to download DALL-E image: HTTP {image_response.status_code}")
            return False, None
            
    except Exception as e:
        logger.error(f"Error generating DALL-E image: {str(e)}")
        return False, None


def create_astrology_image(system_number, current_date, title, width=800, height=600):
    """
    Create an astrology-themed image with the given title
    Returns the filename of the created image (relative path for database storage)
    
    If OPENAI_API_KEY is set, will attempt to generate image with DALL-E 3
    Otherwise, will fall back to local generation
    """
    # Ensure directory exists
    upload_dir = os.path.join(app.root_path, 'static', 'uploads', 'blog')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Create a unique filename based on the system number and current date
    date_str = current_date.strftime("%Y%m%d")
    filename = f"astro_{system_number}_{date_str}.png"
    full_path = os.path.join(upload_dir, filename)
    
    # Get the appropriate system name for this astrology system
    astro_systems = [
        "European Astrology", 
        "Chinese Astrology",
        "Indian Astrology",
        "Lal Kitab",
        "Jyotish",
        "Numerology",
        "Tarot",
        "Planetary Astrology"
    ]
    system_name = astro_systems[(system_number-1) % len(astro_systems)]
    
    # Try to use DALL-E 3 if we have an API key and it's enabled
    use_dalle = bool(os.getenv('OPENAI_API_KEY', '')) and bool(os.getenv('USE_DALLE_IMAGES', 'true').lower() == 'true')
    
    if use_dalle:
        # Try generating with DALL-E
        success, result = generate_dalle_image(
            system_name=system_name,
            title=title,
            current_date=current_date,
            upload_dir=upload_dir,
            filename=filename,
            width=1024,
            height=1024
        )
        
        if success:
            # DALL-E generation successful
            return filename
            
        logger.warning(f"DALL-E image generation failed for {system_name}, falling back to local generation")
    
    # Fallback to local image generation if DALL-E fails or is disabled
    logger.info(f"Using local image generation for {system_name}")
    
    # Use different base colors for different astrology systems
    base_colors = [
        (25, 25, 45),    # Dark blue (European)
        (45, 20, 40),    # Purple (Chinese)
        (40, 30, 20),    # Brown (Indian)
        (20, 40, 30),    # Dark green (Lal Kitab)
        (35, 25, 35),    # Dark violet (Jyotish)
        (45, 35, 20),    # Gold (Numerology)
        (25, 35, 45),    # Blue (Tarot)
        (30, 20, 40),    # Deep purple (Planetary)
    ]
    
    color_index = (system_number - 1) % len(base_colors)
    img = Image.new('RGB', (width, height), color=base_colors[color_index])
    draw = ImageDraw.Draw(img)
    
    # Add stars
    for _ in range(300):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)
        brightness = random.randint(150, 255)
        draw.ellipse((x, y, x + size, y + size), fill=(brightness, brightness, brightness))
    
    # Add zodiac constellation-like patterns
    for _ in range(5):
        points = []
        for i in range(random.randint(5, 10)):
            x = random.randint(50, width-50)
            y = random.randint(50, height-50)
            points.append((x, y))
            # Draw a brighter star at constellation points
            draw.ellipse((x-2, y-2, x+2, y+2), fill=(255, 255, 255))
        
        # Connect constellation points
        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill=(100, 100, 220), width=1)
    
    # Add a central cosmic element (like a planet or moon)
    center_x, center_y = width // 2, height // 2
    radius = random.randint(40, 80)
      # Different colors for different astrology systems with their names
    colors = [
        (120, 100, 220),  # Purple-blue (European)
        (220, 100, 100),  # Red-pink (Chinese)
        (100, 220, 180),  # Turquoise (Indian)
        (220, 180, 100),  # Gold (Lal Kitab)        (170, 100, 220),  # Violet (Jyotish)
        (100, 170, 220),  # Blue (Numerology)
        (220, 140, 80),   # Orange (Tarot)
        (80, 220, 120)    # Green (Planetary)
    ]
    color_index = (system_number - 1) % len(colors)
    color = colors[color_index]
    
    # Create more interesting planet/celestial object
    draw.ellipse((center_x-radius, center_y-radius, center_x+radius, center_y+radius), fill=color)
    
    # Add rings to some planets (for even-numbered systems)
    if system_number % 2 == 0:
        ring_width = radius * 1.8
        ring_height = radius * 0.4
        draw.ellipse(
            (center_x-ring_width/2, center_y-ring_height/2, 
             center_x+ring_width/2, center_y+ring_height/2), 
            outline=(200, 200, 240), width=3
        )
    
    # Add a small moon for odd-numbered systems
    if system_number % 2 == 1:
        moon_radius = radius // 4
        moon_x = center_x + radius + moon_radius
        moon_y = center_y - radius // 2
        draw.ellipse(
            (moon_x-moon_radius, moon_y-moon_radius, 
             moon_x+moon_radius, moon_y+moon_radius),
            fill=(240, 240, 200)
        )
    
    # Try to load a font, use default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 36)
        small_font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Add title text
    text_width = draw.textlength(title, font=font)
    draw.text(((width-text_width)//2, height-100), title, fill=(255, 255, 255), font=font)
      # Get system name based on system_number
    astro_systems = [
        "European Astrology", 
        "Chinese Astrology",
        "Indian Astrology",
        "Lal Kitab",
        "Jyotish",
        "Numerology",
        "Tarot",
        "Planetary Astrology"
    ]
    system_name = astro_systems[(system_number-1) % len(astro_systems)]
    
    # Add the system name at the bottom
    subtitle = system_name
    subtitle_width = draw.textlength(subtitle, font=small_font)
    draw.text(((width-subtitle_width)//2, height-50), subtitle, fill=(200, 200, 255), font=small_font)
    
    # Save the image
    img.save(full_path)
    logger.info(f"Created image for system {system_number} ({system_name}): {filename}")
    
    return filename

def get_assistant_id_for_system(position):
    """
    Get the OpenAI assistant ID for the given astrology system position
    
    Args:
        position (int): The system position (1-8)
        
    Returns:
        str: The assistant ID from environment variables or None if not found
    """
    # Map positions to environment variable names
    system_env_map = {
        1: 'EUROPEAN_ASTROLOGY_ASSISTANT_ID',
        2: 'CHINESE_ASTROLOGY_ASSISTANT_ID',
        3: 'INDIAN_ASTROLOGY_ASSISTANT_ID',
        4: 'NUMEROLOGY_ASSISTANT_ID',
        5: 'TAROT_ASSISTANT_ID',
        6: 'LAL_KITAB_ASSISTANT_ID',  # Using Lal Kitab for Karmic astrology
        7: 'JYOTISH_ASSISTANT_ID',    # Using Jyotish for Esoteric astrology
        8: 'PLANETARY_ASTROLOGY_ASSISTANT_ID'
    }
    
    # Get the environment variable name for this position
    env_var = system_env_map.get(position)
    if not env_var:
        return None
        
    # Return the assistant ID from environment
    return os.environ.get(env_var)

def generate_horoscope_content(system_name, position, current_date):
    """
    Generate horoscope content using OpenAI Assistant API
    
    Args:
        system_name (str): Name of the astrology system
        position (int): The system position (1-8)
        current_date: Current date for the horoscope
        
    Returns:
        dict: A dictionary with title, content and summary
    """
    # Default fallback content in case the API call fails
    date_str = current_date.strftime("%Y-%m-%d")
    title = f"Гороскоп {system_name} на {date_str}"
    
    fallback_content = f"""
    <p>Сьогодні зірки віщують важливі зміни. День сприятливий для початку нових проектів 
    та налагодження стосунків. Зверніть увагу на своє здоров'я та не забувайте 
    про відпочинок.</p>
    <p>Можливі несподівані приємні новини в особистому житті. 
    Фінансове становище стабільне, але варто утриматися від великих витрат.</p>
    """
    
    fallback_summary = "Сприятливий день для важливих рішень та нових починань. Зірки на вашому боці!"
    
    # Get the assistant ID for this system
    assistant_id = get_assistant_id_for_system(position)
    
    # If no assistant ID is configured, return fallback content
    if not assistant_id:
        logger.warning(f"No assistant ID configured for system {position}: {system_name}. Using fallback content.")
        return {
            "title": title,
            "content": fallback_content,
            "summary": fallback_summary
        }
    
    try:
        logger.info(f"Generating horoscope with assistant {assistant_id} for {system_name}")
        
        # Initialize OpenAI client
        client = OpenAI()
        
        # Create a thread for the conversation
        thread = client.beta.threads.create()
        
        # Format the date for the prompt
        prompt_date = current_date.strftime("%d.%m.%Y")
        
        # Create a message for the assistant
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Створи ґрунтовний гороскоп у системі {system_name} на {prompt_date}. "
                    f"Включи усі 12 знаків зодіаку з корисними порадами для кожного знаку. "
                    f"Додай загальну інформацію про астрологічні впливи на цей день."
        )
        
        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        
        # Poll for completion
        for attempt in range(30):  # Timeout after 30 attempts
            time.sleep(3)  # Check every 3 seconds
            
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            
            if run_status.status == 'completed':
                # Get the response
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                generated_content = ""
                
                # Extract content from the first assistant message
                for msg in messages.data:
                    if msg.role == "assistant":
                        for content_item in msg.content:
                            if content_item.type == "text":
                                generated_content = content_item.text.value
                                break
                        break
                
                # Clean up the content for HTML display
                generated_content = generated_content.strip()
                
                # Basic HTML wrapping if needed
                if not generated_content.startswith("<"):
                    paragraphs = generated_content.split("\n\n")
                    formatted_content = ""
                    for p in paragraphs:
                        if p.strip():
                            formatted_content += f"<p>{p.strip()}</p>\n"
                    generated_content = formatted_content
                
                # Extract the first paragraph or portion for summary
                # Remove HTML tags for summary text
                text_content = re.sub('<[^<]+?>', '', generated_content)
                summary_text = text_content.strip().split('\n')[0][:200]
                if len(summary_text) >= 197:
                    summary_text = summary_text[:197] + "..."
                
                logger.info(f"Successfully generated horoscope content for {system_name}")
                
                return {
                    "title": title,
                    "content": generated_content,
                    "summary": summary_text
                }
                
            elif run_status.status == 'failed':
                logger.error(f"Assistant run failed for {system_name}: {run_status.last_error}")
                break
                
            # Continue polling
        
        # If we get here, the assistant did not complete in time
        logger.warning(f"Assistant run timed out for {system_name}. Using fallback content.")
        
    except Exception as e:
        logger.error(f"Error generating horoscope for {system_name}: {str(e)}")
    
    # Return fallback content if anything fails
    return {
        "title": title,
        "content": fallback_content,
        "summary": fallback_summary
    }

def generate_daily_horoscopes():
    """Generate daily horoscopes for all 8 astrology systems with complete replacement of old data"""
    logger.info("Initializing daily horoscope generator with image replacement mode")
    
    try:
        current_date = datetime.utcnow()
        date_str = current_date.strftime("%Y-%m-%d")
        logger.info(f"Generating horoscopes for date: {date_str}")
        
        systems = [
            {"name": "Західна астрологія", "position": 1},
            {"name": "Китайська астрологія", "position": 2},
            {"name": "Ведична астрологія", "position": 3},
            {"name": "Нумерологія", "position": 4},
            {"name": "Таро", "position": 5},
            {"name": "Кармічна астрологія", "position": 6},
            {"name": "Езотерична астрологія", "position": 7},
            {"name": "Світла прогностика", "position": 8}
        ]
        
        # Get all columns for BlogBlock model to check which ones exist
        columns = {}
        with app.app_context():
            insp = inspect(db.engine)
            columns = {column['name']: column for column in insp.get_columns('blog_block')}
            logger.info(f"Found {len(columns)} columns in blog_block table")
        
        # Track image filenames we create
        created_images = []
        
        # Process each astrology system
        for system in systems:
            try:
                position = system['position']
                system_name = system['name']
                
                logger.info(f"Generating horoscope for system {position}: {system_name}")
                
                # Generate horoscope content using OpenAI assistant
                horoscope_data = generate_horoscope_content(system_name, position, current_date)
                
                title = horoscope_data["title"]
                content = horoscope_data["content"]
                summary = horoscope_data["summary"]
                
                # Create the image
                image_filename = create_astrology_image(position, current_date, title)
                created_images.append(image_filename)
                
                with app.app_context():
                    # Get existing block or create new one
                    block = BlogBlock.query.filter_by(position=position).first()
                    
                    if not block:
                        logger.info(f"Creating new block for position {position}")
                        block = BlogBlock(
                            title=title,
                            content=content,
                            summary=summary,
                            position=position,
                            is_active=True,
                            created_at=datetime.utcnow(),
                            featured_image=image_filename
                        )
                        db.session.add(block)
                    else:
                        logger.info(f"Replacing content for position {position}")
                        
                        # Store old image filename for cleanup
                        old_image = block.featured_image
                        
                        # Update basic fields using ORM
                        block.title = title
                        block.content = content
                        block.summary = summary
                        block.updated_at = datetime.utcnow()
                        block.featured_image = image_filename
                          # Update multi-language fields - Ukrainian is default
                        # Use hasattr for safety
                        if 'title_ua' in columns and hasattr(block, 'title_ua'):
                            block.title_ua = title
                            
                        if 'content_ua' in columns and hasattr(block, 'content_ua'):
                            block.content_ua = content
                            
                        if 'summary_ua' in columns and hasattr(block, 'summary_ua'):
                            block.summary_ua = summary
                            
                        # Translate to other languages if enabled
                        use_translations = bool(os.getenv('USE_TRANSLATIONS', 'true').lower() == 'true')
                        
                        if use_translations:
                            # Initialize the translator
                            translator = HoroscopeTranslator()
                            
                            # Only proceed if translation service is available
                            if translator.is_available():
                                # Translate content for each supported language
                                for lang_code in ['en', 'de', 'ru']:
                                    logger.info(f"Translating content to {lang_code} for block {position}")
                                    
                                    # Translate content
                                    content_result = translator.translate_content(content, lang_code)
                                    if content_result.get('success'):
                                        # Set content based on language
                                        content_field = f"content_{lang_code}"
                                        if content_field in columns and hasattr(block, content_field):
                                            setattr(block, content_field, content_result.get('content'))
                                            logger.info(f"Successfully translated content to {lang_code}")
                                        
                                    # Translate title
                                    title_result = translator.translate_content(title, lang_code)
                                    if title_result.get('success'):
                                        # Set title based on language
                                        title_field = f"title_{lang_code}"
                                        if title_field in columns and hasattr(block, title_field):
                                            setattr(block, title_field, title_result.get('content'))
                                    
                                    # Translate summary if it exists
                                    if summary:
                                        summary_result = translator.translate_content(summary, lang_code)
                                        if summary_result.get('success'):
                                            # Set summary based on language
                                            summary_field = f"summary_{lang_code}"
                                            if summary_field in columns and hasattr(block, summary_field):
                                                setattr(block, summary_field, summary_result.get('content'))
                            else:
                                logger.warning("Translation service not available - skipping translations")
                    
                    # Commit changes for this block
                    db.session.commit()
                    logger.info(f"Successfully updated block {position} with replacement horoscope and image")
                    
            except Exception as e:
                logger.error(f"Error processing system {system['position']}: {str(e)}")
          # After all horoscopes are generated and database updated, clean up old images
        # Only keep the most current ones we just created
        position_numbers = [system["position"] for system in systems]
        
        # Force cleanup of ALL old horoscope images except the current ones
        from force_cleanup_horoscope_images import force_cleanup_images
        num_deleted = force_cleanup_images()
        logger.info(f"Force deleted {num_deleted} old horoscope images")
                
        logger.info("Daily horoscope replacement completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error in horoscope generation: {str(e)}")
        return False

if __name__ == "__main__":
    # Run generator with replacement mode
    success = generate_daily_horoscopes()
    sys.exit(0 if success else 1)
