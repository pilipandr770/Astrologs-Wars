import os
import sys
import logging
from urllib.parse import urlparse
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    filename='horoscope_generator.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("HoroscopeGenerator")

# Load environment variables from .env file
load_dotenv()

# Verify and clean the DATABASE_URL to prevent connection issues
db_url = os.getenv('DATABASE_URL')
if not db_url:
    logger.error("DATABASE_URL environment variable is not set")
    sys.exit(1)

# Strip any whitespace or newlines that might cause connection issues
db_url = db_url.strip()
logger.info(f"Using database URL: {db_url.replace(urlparse(db_url).password, '****')}")

# Continue with imports after environment setup to avoid import errors
try:
    from app import create_app
    from app.models import HoroscopeBlock, BlogBlock, db
    from datetime import datetime, timedelta
    import random
    import openai
    import time
    import re
    from markdownify import markdownify as md
    import requests
    
    logger.info("All modules imported successfully")
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)

# Initialize the Flask application to get the database context
try:
    app = create_app()
    logger.info("Flask application initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Flask application: {e}")
    sys.exit(1)

# Function declarations and script continues here...
