from app import create_app
import os
from PIL import Image, ImageDraw, ImageFont
import random
import uuid
import glob

app = create_app()

def create_astrology_image(title, filename, width=800, height=600):
    """Create an astrology-themed image with the given title"""
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
    radius = random.randint(40, 80)    # Create a simple planet circle
    color = (120, 100, 220)  # Purple-blue color
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
    img.save(filename)
    return filename

def main():
    """Create placeholder images for astrology products"""
    upload_dir = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Create images for specific products
    products = [
        "monthly_horoscope.jpg",
        "natal_chart.jpg", 
        "annual_forecast.jpg"
    ]
    
    titles = [
        "Monthly Horoscope",
        "Natal Chart Analysis",
        "Annual Forecast"
    ]
    
    for i, product in enumerate(products):
        filename = os.path.join(upload_dir, str(uuid.uuid4()) + '.jpg')
        create_astrology_image(titles[i], filename)
        print(f"Created image: {filename}")
        
        # Rename existing product images with this name to use the new image
        old_files = glob.glob(os.path.join(upload_dir, '*'))
        for old_file in old_files:
            if os.path.basename(old_file) != os.path.basename(filename):
                if product in old_file or products[i].replace('.jpg', '') in old_file:
                    # We found an old file that matches our product
                    # So we rename our new file to match its name
                    os.rename(filename, old_file)
                    filename = old_file
                    print(f"Renamed to: {old_file}")
                    break

if __name__ == '__main__':
    main()
    print("Placeholder images created successfully!")
