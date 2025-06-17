"""
Script to verify all blog-related fixes
"""
from app import create_app, db
from app.models import BlogBlock
from app.utils.text_utils import strip_html_tags
import os

def check_blog_fixes():
    app = create_app()
    
    with app.app_context():
        print("=== BLOG FIXES VERIFICATION ===")
        
        # Check for active blocks
        active_blocks = BlogBlock.query.filter_by(is_active=True).order_by(BlogBlock.position).all()
        print(f"Total active blocks: {len(active_blocks)}")
        
        # Check active horoscope blocks (position 1-8)
        horoscope_blocks = BlogBlock.query.filter(
            BlogBlock.is_active == True,
            BlogBlock.position.between(1, 8)
        ).order_by(BlogBlock.position).all()
        
        print(f"Active horoscope blocks: {len(horoscope_blocks)}")
        
        # Check for shop block
        shop_block = BlogBlock.query.filter_by(position=12, is_active=True).first()
        print(f"Shop block active: {shop_block is not None}")
        
        # Test HTML stripping
        print("\n=== HTML STRIPPING TEST ===")
        for block in horoscope_blocks[:2]:  # Just check first two blocks
            original = block.summary
            stripped = strip_html_tags(original)
            print(f"Block {block.position} - Original: '{original[:50]}...'")
            print(f"Block {block.position} - Stripped: '{stripped[:50]}...'")
            
        # Check template files
        print("\n=== TEMPLATE FILES CHECK ===")
        template_path = os.path.join(app.root_path, 'templates', 'blog')
        blog_templates = os.listdir(template_path)
        print(f"Blog templates: {blog_templates}")
        
        # Possible duplicate files
        duplicate_check = [f for f in blog_templates if 'index_' in f or '.new' in f]
        if duplicate_check:
            print(f"WARNING: Possible duplicate files: {duplicate_check}")
        else:
            print("No duplicate templates found")

if __name__ == "__main__":
    check_blog_fixes()
