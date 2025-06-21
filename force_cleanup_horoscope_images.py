"""
Скрипт для принудительного удаления старых изображений гороскопов
"""
import os
import glob
import sys
import logging
from datetime import datetime

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

# Import app after logging setup
from app import create_app

def force_cleanup_images():
    """
    Удаляет все гороскопные изображения кроме самых последних
    """
    app = create_app()
    logger.info("Starting forced cleanup of horoscope images")
    
    # Get current date
    current_date = datetime.utcnow()
    date_str = current_date.strftime("%Y%m%d")
    
    # Get the uploads directory
    upload_dir = os.path.join(app.root_path, 'static', 'uploads', 'blog')
    if not os.path.exists(upload_dir):
        logger.warning(f"Blog uploads directory doesn't exist: {upload_dir}")
        return 0
        
    # Get list of all astro image files
    horoscope_image_pattern = os.path.join(upload_dir, "astro_*.png")
    image_files = glob.glob(horoscope_image_pattern)
    
    # Keep track of what we're keeping and deleting
    files_to_keep = []
    files_to_delete = []
    
    # First pass - identify the latest files for each position
    latest_files = {}
    
    for image_path in image_files:
        filename = os.path.basename(image_path)
        
        # Parse the filename (format: astro_1_20250621.png)
        parts = filename.split('_')
        if len(parts) == 3:
            position = parts[1]
            date_part = parts[2].split('.')[0]
            
            # Keep track of the latest file for each position
            if position not in latest_files or date_part > latest_files[position][1]:
                latest_files[position] = (filename, date_part, image_path)
    
    # Second pass - delete all files except the latest for each position
    deleted_count = 0
    
    for image_path in image_files:
        filename = os.path.basename(image_path)
        
        # Check if this file is in our latest_files dict
        keep_file = False
        for pos in latest_files:
            if filename == latest_files[pos][0]:
                keep_file = True
                break
                
        if not keep_file:
            try:
                os.remove(image_path)
                deleted_count += 1
                logger.info(f"Deleted old image: {filename}")
            except Exception as e:
                logger.error(f"Failed to delete {filename}: {str(e)}")
    
    logger.info(f"Forced cleanup complete: Deleted {deleted_count} old horoscope images")
    return deleted_count

if __name__ == "__main__":
    num_deleted = force_cleanup_images()
    print(f"Удалено {num_deleted} старых изображений гороскопов.")
