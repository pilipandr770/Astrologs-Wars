"""
Script to generate missing horoscope images for the active blog blocks
"""
from app import create_app, db
from app.models import BlogBlock
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random

def create_astrology_image(title, filename, position, width=800, height=600):
    """Create an astrology-themed image with the given title"""
    # Create a new image with a starry sky background (different color based on position)
    # Use different base colors for different astrology systems
    base_colors = [
        (25, 25, 45),    # Dark blue
        (45, 20, 40),    # Purple
        (40, 30, 20),    # Brown
        (20, 40, 30),    # Dark green
        (35, 25, 35),    # Dark violet
        (45, 35, 20),    # Gold
        (25, 35, 45),    # Blue
        (30, 20, 40),    # Deep purple
    ]
    
    color_index = (position - 1) % len(base_colors)
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
    
    # Different colors for different systems
    planet_colors = [
        (120, 100, 220),  # Purple-blue
        (220, 120, 100),  # Orange-red
        (100, 220, 120),  # Green
        (220, 180, 100),  # Gold
        (100, 180, 220),  # Blue
        (180, 100, 220),  # Purple
        (180, 220, 100),  # Yellow-green
        (220, 100, 180),  # Pink
    ]
    color_index = (position - 1) % len(planet_colors)
    color = planet_colors[color_index]
    
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
    
    # Add the position identifier
    subtitle = f"Astrological System #{position}"
    subtitle_width = draw.textlength(subtitle, font=small_font)
    draw.text(((width-subtitle_width)//2, height-50), subtitle, fill=(200, 200, 255), font=small_font)
    
    # Save the image
    img.save(filename)
    print(f"Created image: {filename}")
    return filename

def main():
    """Generate horoscope images for all active blog blocks"""
    app = create_app()
    
    with app.app_context():
        # Ensure uploads directory exists
        upload_dir = os.path.join(app.root_path, 'static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Create blog images directory if it doesn't exist
        blog_upload_dir = os.path.join(upload_dir, 'blog')
        os.makedirs(blog_upload_dir, exist_ok=True)
        
        print("Checking blog blocks for missing images...")
        # Get all active blog blocks in positions 1-8 (horoscope blocks)
        blocks = BlogBlock.query.filter(
            BlogBlock.is_active == True,
            BlogBlock.position.between(1, 8)        ).order_by(BlogBlock.position).all()
        
        today = datetime.now().strftime("%Y%m%d")
        
        for block in blocks:
            # Generate image filename based on position and date
            image_filename = f"astro_{block.position}_{today}.png"
            
            # Check if the block already has an image
            if block.featured_image and os.path.exists(os.path.join(blog_upload_dir, block.featured_image)) and block.position != 2:
                print(f"Block {block.position} already has image: {block.featured_image}")
                continue
                
            # Force regeneration for block #2
            if block.position == 2:
                print(f"Forcing regeneration of image for block #2")
            
            # Create the image
            title = block.title or f"Астрологічна система #{block.position}"
            image_path = os.path.join(blog_upload_dir, image_filename)
            
            # Create the astrology image
            create_astrology_image(title, image_path, block.position)
            
            # Update the block with the new image filename
            block.featured_image = image_filename
            print(f"Updated block {block.position} with image: {image_filename}")
            
        # Commit changes to the database
        db.session.commit()
        print("All horoscope blocks updated with images.")

if __name__ == '__main__':
    main()
