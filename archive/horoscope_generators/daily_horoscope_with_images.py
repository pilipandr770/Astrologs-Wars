"""
Скрипт для ежедневной генерации гороскопов с интегрированной генерацией изображений.
Объединяет функционал daily_horoscope_sql_fix.py и create_astro_images.py.
"""
import os
import time
import json
import sys
import re
import logging
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import urlparse
from sqlalchemy import inspect, text
from PIL import Image, ImageDraw, ImageFont
import random
import uuid

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
logger.info("Starting horoscope generator script with image creation")

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

# Import app only after setting environment variables
from app import create_app, db
from app.models import BlogBlock

app = create_app()

def create_astrology_image(system_number, current_date, title, width=800, height=600):
    """
    Create an astrology-themed image with the given title
    Returns the filename of the created image (relative path for database storage)
    """
    # Ensure directory exists
    upload_dir = os.path.join(app.root_path, 'static', 'uploads', 'blog')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Create a unique filename based on the system number and current date
    date_str = current_date.strftime("%Y%m%d")
    filename = f"astro_{system_number}_{date_str}.png"
    full_path = os.path.join(upload_dir, filename)
    
    # Create a new image with a starry sky background
    img = Image.new('RGB', (width, height), color=(25, 25, 45))
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
    
    # Different colors for different astrology systems
    colors = [
        (120, 100, 220),  # Purple-blue
        (220, 100, 100),  # Red-pink
        (100, 220, 180),  # Turquoise
        (220, 180, 100),  # Gold
        (170, 100, 220),  # Violet
        (100, 170, 220),  # Blue
        (220, 140, 80),   # Orange
        (80, 220, 120)    # Green
    ]
    color_index = (system_number - 1) % len(colors)
    color = colors[color_index]
    
    draw.ellipse((center_x-radius, center_y-radius, center_x+radius, center_y+radius), fill=color)
    
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
    
    # Add the word "Astrology" at the bottom
    subtitle = "Astrological Forecast"
    subtitle_width = draw.textlength(subtitle, font=small_font)
    draw.text(((width-subtitle_width)//2, height-50), subtitle, fill=(200, 200, 255), font=small_font)
    
    # Save the image
    img.save(full_path)
    logger.info(f"Created image for system {system_number}: {filename}")
    
    return filename

def generate_daily_horoscopes():
    """Generate daily horoscopes for all 8 astrology systems"""
    logger.info("Initializing daily horoscope generator with images")
    
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
        
        # Process each astrology system
        for system in systems:
            try:
                position = system['position']
                system_name = system['name']
                
                logger.info(f"Generating horoscope for system {position}: {system_name}")
                
                # Sample horoscope content - in production replace with actual API call
                title = f"Гороскоп {system_name} на {date_str}"
                content = f"""
                <p>Сьогодні зірки віщують важливі зміни. День сприятливий для початку нових проектів 
                та налагодження стосунків. Зверніть увагу на своє здоров'я та не забувайте 
                про відпочинок.</p>
                <p>Можливі несподівані приємні новини в особистому житті. 
                Фінансове становище стабільне, але варто утриматися від великих витрат.</p>
                """
                summary = "Сприятливий день для важливих рішень та нових починань. Зірки на вашому боці!"
                
                # Create the image
                image_filename = create_astrology_image(position, current_date, title)
                
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
                        logger.info(f"Updating existing block for position {position}")
                        # Update basic fields using ORM
                        block.title = title
                        block.content = content
                        block.summary = summary
                        block.updated_at = datetime.utcnow()
                        block.featured_image = image_filename
                        
                        # Update multi-language fields
                        # Use hasattr for safety
                        if 'title_ua' in columns and hasattr(block, 'title_ua'):
                            block.title_ua = title
                            
                        if 'content_ua' in columns and hasattr(block, 'content_ua'):
                            block.content_ua = content
                            
                        if 'summary_ua' in columns and hasattr(block, 'summary_ua'):
                            block.summary_ua = summary
                    
                    db.session.commit()
                    logger.info(f"Successfully updated block {position} with new horoscope and image")
                    
            except Exception as e:
                logger.error(f"Error processing system {system['position']}: {str(e)}")
                
        logger.info("Daily horoscope generation completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error in horoscope generation: {str(e)}")
        return False

if __name__ == "__main__":
    # Run generator
    success = generate_daily_horoscopes()
    sys.exit(0 if success else 1)
