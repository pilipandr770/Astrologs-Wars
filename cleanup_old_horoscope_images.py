"""
Script to clean up old horoscope images to save disk space
"""
import os
import sys
import logging
from datetime import datetime, timedelta
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("horoscope_cleanup.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("HoroscopeCleanup")

def cleanup_old_images(days_to_keep=30):
    """Clean up horoscope images older than the specified number of days"""
    app = create_app()
    
    # Calculate the cutoff date
    cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
    logger.info(f"Cleaning up horoscope images older than {days_to_keep} days ({cutoff_date.strftime('%Y-%m-%d')})")
    
    # Get path to blog images directory
    blog_dir = os.path.join(app.root_path, 'static', 'uploads', 'blog')
    
    if not os.path.exists(blog_dir):
        logger.error(f"Blog directory does not exist: {blog_dir}")
        return False
    
    # Get list of astro image files
    files = [f for f in os.listdir(blog_dir) if f.startswith('astro_') and f.endswith('.png')]
    logger.info(f"Found {len(files)} horoscope images")
    
    # Track statistics
    deleted_count = 0
    kept_count = 0
    error_count = 0
    
    for filename in files:
        try:
            # Extract date from filename (format: astro_1_20250621.png)
            date_part = filename.split('_')[2].split('.')[0]  # Gets the date: "20250621"
            
            # Parse the date
            file_date = datetime.strptime(date_part, "%Y%m%d")
            
            # Check if older than cutoff
            if file_date < cutoff_date:
                file_path = os.path.join(blog_dir, filename)
                os.remove(file_path)
                logger.info(f"Deleted old image: {filename}")
                deleted_count += 1
            else:
                kept_count += 1
                
        except Exception as e:
            logger.error(f"Error processing file {filename}: {str(e)}")
            error_count += 1
    
    logger.info(f"Cleanup complete: {deleted_count} deleted, {kept_count} kept, {error_count} errors")
    return True

if __name__ == "__main__":
    # Get days to keep from command line argument, default to 30 days
    days = 30
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except ValueError:
            logger.error(f"Invalid days parameter: {sys.argv[1]}. Using default of 30 days.")
    
    cleanup_old_images(days)
