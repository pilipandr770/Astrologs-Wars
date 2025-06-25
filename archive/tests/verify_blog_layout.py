"""
Script to verify blog blocks layout
"""
from app import create_app, db
from app.models import BlogBlock
from app.utils.text_utils import strip_html_tags

def verify_blog_layout():
    print("Verifying blog blocks layout...")
    app = create_app()
    
    with app.app_context():
        # Check total active blocks
        all_active_blocks = BlogBlock.query.filter_by(is_active=True).all()
        print(f"Total active blocks: {len(all_active_blocks)}")
        
        # Check horoscope blocks (positions 1-8)
        horoscope_blocks = BlogBlock.query.filter_by(is_active=True).filter(BlogBlock.position <= 8).order_by(BlogBlock.position).all()
        print(f"Active horoscope blocks (positions 1-8): {len(horoscope_blocks)}")
        
        # Ensure exactly 8 horoscope blocks are active
        if len(horoscope_blocks) < 8:
            print("WARNING: Less than 8 active horoscope blocks found!")
            
            # Check which positions are missing
            positions = [block.position for block in horoscope_blocks]
            for i in range(1, 9):
                if i not in positions:
                    print(f"Missing block at position {i}")
                    
                    # Get the block if it exists but is inactive
                    inactive_block = BlogBlock.query.filter_by(position=i).first()
                    if inactive_block:
                        print(f"  Found inactive block at position {i}, activating it...")
                        inactive_block.is_active = True
                    else:
                        print(f"  Creating new block for position {i}...")
                        new_block = BlogBlock(
                            title=f"Астрологічна система #{i}",
                            content=f"Текст для астрологічної системи #{i}",
                            summary=f"Короткий опис для астрологічної системи #{i}",
                            position=i,
                            is_active=True
                        )
                        db.session.add(new_block)
            
            db.session.commit()
            print("Horoscope blocks updated!")
        
        # Check for shop block
        shop_block = BlogBlock.query.filter_by(position=12).first()
        if shop_block:
            print(f"Shop block exists (position 12), active: {shop_block.is_active}")
        else:
            print("No shop block found at position 12")
        
        # Verify the text content of each block (first few characters)
        print("\nHoroscope block content preview:")
        for block in BlogBlock.query.filter(BlogBlock.position <= 8).order_by(BlogBlock.position).all():
            clean_summary = strip_html_tags(block.summary or "")
            print(f"Block {block.position} - Active: {block.is_active} - Title: {block.title[:30]} - Summary: {clean_summary[:30]}...")

if __name__ == "__main__":
    verify_blog_layout()
