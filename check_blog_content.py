"""
Check content of blog blocks
"""
from app import create_app
from app.models import BlogBlock

app = create_app()

def check_if_empty(text):
    """Check if text is empty or contains only whitespace"""
    if text is None:
        return True
    return text.strip() == ""

with app.app_context():
    blocks = BlogBlock.query.filter_by(is_active=True).order_by(BlogBlock.position).all()
    
    for block in blocks:
        print(f"Block {block.position} ({block.title}):")
        print(f"  Content empty? {check_if_empty(block.content)}")
        print(f"  Summary empty? {check_if_empty(block.summary)}")
        print("-" * 50)
