"""
Script to check if horoscope blocks have been updated with the correct image paths
"""
from app import create_app, db
from app.models import BlogBlock
from datetime import datetime

def check_horoscope_block_images():
    """Check if horoscope blocks have correct images assigned"""
    app = create_app()
    
    with app.app_context():
        print("Checking horoscope block images...")
        print("-" * 60)
        print(f"{'Position':<10} {'Title':<30} {'Image Path':<30} {'Updated'}")
        print("-" * 60)
        
        # Check each position from 1 to 8
        for position in range(1, 9):
            block = BlogBlock.query.filter_by(position=position).first()
            
            if block:
                # Format last updated date
                updated = block.updated_at.strftime("%Y-%m-%d %H:%M") if block.updated_at else "N/A"
                
                # Truncate title if too long
                title = block.title[:27] + "..." if len(block.title) > 30 else block.title
                
                print(f"{position:<10} {title:<30} {block.featured_image or 'No image':<30} {updated}")
            else:
                print(f"{position:<10} {'Block not found':<30} {'N/A':<30} {'N/A'}")
        
        print("-" * 60)

if __name__ == "__main__":
    check_horoscope_block_images()
